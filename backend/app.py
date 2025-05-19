from flask import Flask, redirect, url_for, session, jsonify, send_from_directory, request, abort
from dotenv import load_dotenv
from functools import wraps
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
# Load environment variables (.env cannot be automatically loaded)
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env')))
env = os.getenv('FLASK_ENV', 'development')
if env == 'development':
   load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env.dev')))
    
if env == 'production':
    load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env.prod')))

# Initialize Flask app
app = Flask(__name__, static_folder=static_path, template_folder=template_path)
NYT_API_KEY = os.getenv("NYT_API_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

if env == 'development':
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
else:
    app.secret_key = os.urandom(24)

# Enable CORS for API endpoints
CORS(app,
     supports_credentials=True,
     origins=["http://localhost:5173", "http://127.0.0.1:5173"])

# Secret key for session management



#initial OAuth
oauth = OAuth(app)

nonce = generate_token()


oauth.register(
    name='flask_app',
    client_id='flask-app',
    client_secret='flask-secret',
    # server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            abort(401)
        return f(*args, **kwargs)
    return decorated

#who's logged in?
@app.route("/api/userinfo")
def userinfo():
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify(session["user"])

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f"<h2>Logged in as {user['email']}</h2><a href='/logout'>Logout</a>"
    return '<a href="/login">Login with Dex</a>'

@app.route("/api/ping")
def ping():
    return jsonify({"message": "pong"})

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
    return redirect('http://localhost:5173/')

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"status": "success"}), 200


@app.route('/api/ucdavis-news') # API endpoint to fetch UC Davis–related articles
def get_news():
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22UC%20Davis%22&api-key={NYT_API_KEY}"
    response = requests.get(url)
    data = response.json()
    data['response']['docs'].extend(requests.get(url + "&page=1").json()['response']['docs']) # Combine page 0 and page 1
    return jsonify(data) # Return JSON to client

@app.route("/api/comments")
def get_comments():
    article_id = request.args.get("article_id") # get the article_id from the frontend request
    print("Requested article_id:", article_id)
    docs = mongo.db.comments.find({"article_id": article_id}) # find where the comment are stored in mongoDB database
    out = []
    for c in docs:
        c["_id"] = str(c["_id"])
        out.append(c)
    return jsonify(out)

@app.route("/api/comments", methods=["POST"])
@require_login
def post_comment():
    data = request.get_json()
    content = data.get("content", "").strip()
    parent_id = data.get("parent") # get the parent_id from the frontend, therefore the comment can be nested
    if not content:
        abort(400)
    info = session["user"]
    comment = {
        "article_id": data["article_id"],
        "user":       info["email"],
        "content":    content,
        "created":    datetime.utcnow().isoformat(),
        "removed":    False,
        "parent":     parent_id
    }
    print("Comment:", comment)
    res = mongo.db.comments.insert_one(comment)
    comment["_id"] = str(res.inserted_id)
    return jsonify(comment), 201

# delete method to delete the comment as admin and moderator
@app.route("/api/comments/<cid>", methods=["DELETE"]) # it requires <cid> as a parameter
@require_login
def delete_comment(cid):
    info = session["user"]
    # Check if user is admin or moderator based on name
    if info.get("name") not in ["admin", "moderator"]:
        abort(403)
    
    result = mongo.db.comments.update_one(
        {"_id": ObjectId(cid)},
        {"$set": {
            "content": "COMMENT REMOVED BY MODERATOR!",
            "removed": True
        }}
    )
    
    if result.modified_count == 0:
        abort(404)  # Comment not found
    return "", 204

# put method to update only parts of the comment
@app.route("/api/comments/<cid>", methods=["PUT"]) # it requires <cid> as a parameter
@require_login
def redact_comment(cid):
    info = session["user"]
    if info.get("name") not in ["admin", "moderator"]:
        abort(403)

    data = request.get_json() # get the content from the frontend
    content = data.get("content", "").strip()
    if not content:
        abort(400)

    # replace the selected text with a full block (U+2588).
    redacted = ''.join('█' if c != ' ' else ' ' for c in content)

    # update the content of the comment in the mongodb database
    mongo.db.comments.update_one(
        {"_id": ObjectId(cid)},
        {"$set": {"content": redacted, "removed": False}}
    )
    return jsonify({"status": "redacted"}), 200
    

@app.route('/api/article/<article_id>')
def get_article(article_id):
    try:
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=_id:{article_id}&api-key={NYT_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data['response']['docs']:
            return jsonify(data['response']['docs'][0])
        return jsonify({'error': 'Article not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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