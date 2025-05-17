from flask import Flask, redirect, url_for, session, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
import requests
from flask_cors import CORS


# Configure folder names via environment (with defaults)
static_path = os.getenv('STATIC_PATH','static') # Directory for compiled frontend assets
template_path = os.getenv('TEMPLATE_PATH','templates') # Directory for HTML templates

# Initialize Flask app, telling it where to find static files and templates
app = Flask(__name__, static_folder=static_path, template_folder=template_path)

# Enable CORS for API endpoints
CORS(app)

# Secret key for session management
app.secret_key = os.urandom(24)


#initial OAuth
oauth = OAuth(app)

nonce = generate_token()


oauth.register(
    name=os.getenv('OIDC_CLIENT_NAME'),
    client_id=os.getenv('OIDC_CLIENT_ID'),
    client_secret=os.getenv('OIDC_CLIENT_SECRET'),
    #server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f"<h2>Logged in as {user['email']}</h2><a href='/logout'>Logout</a>"
    return '<a href="/login">Login with Dex</a>'

@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:8000/authorize'
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = oauth.flask_app.parse_id_token(token, nonce=nonce)  # or use .get('userinfo').json()
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/key')
def get_api_key():
    # grab it from the environment
    key = os.getenv('NYT_API_KEY','')
    return jsonify({'api_key': key})

@app.route('/api/ucdavis-news') # API endpoint to fetch UC Davis–related articles
def get_news():
    # Build the request URL with query parameters and API key
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22UC%20Davis%22&api-key=w4rcy5YA6GG99HeECAyyBwmfzARZefFx"
    response = requests.get(url) # Perform HTTP GET
    data = response.json() # Parse response as JSON
    data['response']['docs'].extend(requests.get(url + "&page=1").json()['response']['docs']) # Combine page 0 and page 1
    return jsonify(data) # Return JSON to client

@app.route('/') # Serve index for root
@app.route('/<path:path>') # Serve other frontend routes
def serve_frontend(path=''):
     # If the path matches a file in static folder, serve that file directly
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    # Otherwise, serve the main HTML template
    return send_from_directory(template_path, 'index.html')

if __name__ == '__main__':
    # Determine debug mode from FLASK_ENV
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    # Start Flask development server on specified host and port
    app.run(host='0.0.0.0', 
            port=int(os.environ.get('PORT', 8000)),
            debug=debug_mode
            )