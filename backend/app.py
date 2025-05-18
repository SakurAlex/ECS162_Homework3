from flask import Flask, redirect, url_for, session, jsonify, send_from_directory
from dotenv import load_dotenv

from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
import requests
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime      import datetime


# Configure folder names via environment (with defaults)
static_path = os.getenv('STATIC_PATH','static') # Directory for compiled frontend assets
template_path = os.getenv('TEMPLATE_PATH','templates') # Directory for HTML templates
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env')))


# Initialize Flask app, telling it where to find static files and templates
app = Flask(__name__, static_folder=static_path, template_folder=template_path)
NYT_API_KEY = os.getenv("NYT_API_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Enable CORS for API endpoints
CORS(app,
     supports_credentials=True,
     origins=[os.getenv("VITE_BASE_URL", "http://localhost:5173")])

# Secret key for session management
app.secret_key = os.urandom(24)


#initial OAuth
oauth = OAuth(app)

nonce = generate_token()


oauth.register(
    name=os.getenv('OIDC_CLIENT_NAME'),
    client_id=os.getenv('OIDC_CLIENT_ID'),
    client_secret=os.getenv('OIDC_CLIENT_SECRET'),
    server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

#who's logged in?
@app.route("/api/userinfo")
def userinfo():
    info = oidc.user_getinfo(["email","groups"])
    return jsonify(info)

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


@app.route('/api/ucdavis-news') # API endpoint to fetch UC Davis–related articles
def get_news():
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22UC%20Davis%22&api-key={NYT_API_KEY}"
    response = requests.get(url)
    data = response.json()
    data['response']['docs'].extend(requests.get(url + "&page=1").json()['response']['docs']) # Combine page 0 and page 1
    return jsonify(data) # Return JSON to client

@app.route("/api/comments")
def get_comments():
    article_id = request.args.get("article_id")
    docs = mongo.db.comments.find({"article_id": article_id})
    out = []
    for c in docs:
        c["_id"] = str(c["_id"])
        out.append(c)
    return jsonify(out)

@app.route("/api/comments", methods=["POST"])
@oidc.require_login
def post_comment():
    data = request.get_json()
    content = data.get("content", "").strip()
    if not content:
        abort(400)
    user_email = oidc.user_getinfo(["email"])["email"]
    comment = {
        "article_id": data["article_id"],
        "user":       user_email,
        "content":    content,
        "created":    datetime.utcnow().isoformat(),
        "removed":    False
    }
    res = mongo.db.comments.insert_one(comment)
    comment["_id"] = str(res.inserted_id)
    return jsonify(comment), 201

@app.route("/api/comments/<cid>", methods=["DELETE"])
@oidc.require_login
def delete_comment(cid):
    info = oidc.user_getinfo(["email","groups"])
    if "admin" not in info.get("groups", []):
        abort(403)
    mongo.db.comments.update_one(
        {"_id": ObjectId(cid)},
        {"$set": {
            "content": "COMMENT REMOVED BY MODERATOR!",
            "removed": True
        }}
    )
    return "", 204

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