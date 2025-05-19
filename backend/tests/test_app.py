# backend/tests/test_app.py

import os
import runpy
import pytest
import json
from bson.objectid import ObjectId
import flask
import dotenv

import app

@pytest.fixture
def client():
    # Turn off exception propagation so unhandled errors return 500
    app.app.config["TESTING"] = False
    with app.app.test_client() as client:
        yield client

# ----------------------------------------
# /api/userinfo
# ----------------------------------------
def test_userinfo_not_logged_in(client):
    resp = client.get("/api/userinfo")
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Not logged in"

def test_userinfo_logged_in(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "test@domain", "name": "Tester"}
    resp = client.get("/api/userinfo")
    assert resp.status_code == 200
    assert resp.get_json() == {"email": "test@domain", "name": "Tester"}

# ----------------------------------------
# /
# ----------------------------------------
def test_home_logged_out(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'<a href="/login">' in resp.data

def test_home_logged_in(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "me@u", "name": "Me"}
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Logged in as me@u" in resp.data

# ----------------------------------------
# /api/ping
# ----------------------------------------
def test_ping(client):
    resp = client.get("/api/ping")
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "pong"}

# ----------------------------------------
# /login → nonce + redirect
# /authorize → set session['user']
# /logout clears session
# ----------------------------------------
class DummyLogin:
    def authorize_redirect(self, redirect_uri, nonce):
        return ("REDIRECT_OK", 302)

class DummyAuth:
    def authorize_access_token(self):
        return {"fake_token": True}
    def parse_id_token(self, token, nonce):
        return {"email": "parsed@u", "name": "Parsed"}

def test_login_sets_nonce_and_redirects(monkeypatch, client):
    monkeypatch.setattr(app.oauth.flask_app, "authorize_redirect", DummyLogin().authorize_redirect)
    resp = client.get("/login")
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert "nonce" in sess

def test_authorize_sets_user(monkeypatch, client):
    # preload nonce
    with client.session_transaction() as sess:
        sess["nonce"] = "ABC"
    monkeypatch.setattr(app.oauth.flask_app, "authorize_access_token", DummyAuth().authorize_access_token)
    monkeypatch.setattr(app.oauth.flask_app, "parse_id_token",     DummyAuth().parse_id_token)
    resp = client.get("/authorize")
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert sess["user"] == {"email": "parsed@u", "name": "Parsed"}

def test_logout_clears_session(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "x@y", "name": "X"}
    resp = client.get("/logout")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "success"}
    with client.session_transaction() as sess:
        assert "user" not in sess

# ----------------------------------------
# /api/ucdavis-news
# ----------------------------------------
def test_get_news(monkeypatch, client):
    page0 = {"response": {"docs": [{"_id": 1}]}}
    page1 = {"response": {"docs": [{"_id": 2}]}}
    def fake_get(url):
        if "page=1" in url:
            return type("R", (), {"json": lambda self: page1})()
        return type("R", (), {"json": lambda self: page0})()
    monkeypatch.setattr(app, "requests", type("M", (), {"get": fake_get}))
    resp = client.get("/api/ucdavis-news")
    assert resp.status_code == 200
    docs = resp.get_json()["response"]["docs"]
    assert [d["_id"] for d in docs] == [1, 2]

# ----------------------------------------
# /api/comments?article_id=…
# ----------------------------------------
def test_get_comments(monkeypatch, client):
    dummy = [{ "_id": ObjectId(), "article_id": "A", "content": "hi" }]
    class C:
        def find(self, q): return dummy
    monkeypatch.setattr(app.mongo.db, "comments", C())
    resp = client.get("/api/comments?article_id=A")
    assert resp.status_code == 200
    out = resp.get_json()
    assert isinstance(out, list) and out[0]["article_id"] == "A"

def test_get_comments_no_param(monkeypatch, client):
    # even without ?article_id, it should return []
    class C:
        def find(self, q): return []
    monkeypatch.setattr(app.mongo.db, "comments", C())
    resp = client.get("/api/comments")
    assert resp.status_code == 200
    assert resp.get_json() == []

# ----------------------------------------
# POST /api/comments
# ----------------------------------------
def test_post_comment_unauthenticated(client):
    resp = client.post("/api/comments", json={"article_id": "X", "content": "C"})
    assert resp.status_code == 401

def test_post_comment_bad_request(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "u@u", "name": "U"}
    resp = client.post("/api/comments", json={"article_id": "X", "content": ""})
    assert resp.status_code == 400

def test_post_comment_success(monkeypatch, client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "u@u", "name": "U"}
    class R: inserted_id = ObjectId("507f1f77bcf86cd799439011")
    class C:
        def insert_one(self, d): return R()
    monkeypatch.setattr(app.mongo.db, "comments", C())
    resp = client.post("/api/comments", json={"article_id": "A", "content": "Hello"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["article_id"] == "A" and body["content"] == "Hello"
    assert body["_id"] == str(R.inserted_id)

# ----------------------------------------
# DELETE /api/comments/<cid>
# ----------------------------------------
def test_delete_comment_unauthenticated(client):
    resp = client.delete("/api/comments/507f1f77bcf86cd799439011")
    assert resp.status_code == 401

def test_delete_comment_forbidden(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "x", "name": "notmod"}
    resp = client.delete("/api/comments/507f1f77bcf86cd799439011")
    assert resp.status_code == 403

def test_delete_comment_not_found(monkeypatch, client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "x", "name": "admin"}
    class R: modified_count = 0
    class C:
        def update_one(self, q, u): return R()
    monkeypatch.setattr(app.mongo.db, "comments", C())
    resp = client.delete("/api/comments/507f1f77bcf86cd799439011")
    assert resp.status_code == 404

def test_delete_comment_success(monkeypatch, client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "x", "name": "moderator"}
    class R: modified_count = 1
    class C:
        def update_one(self, q, u): return R()
    monkeypatch.setattr(app.mongo.db, "comments", C())
    resp = client.delete("/api/comments/507f1f77bcf86cd799439011")
    assert resp.status_code == 204
    assert resp.data == b""

# ----------------------------------------
# PUT /api/comments/<cid>
# ----------------------------------------
def test_put_comment_unauthenticated(client):
    resp = client.put("/api/comments/507f1f77bcf86cd799439011", json={"content": "C"})
    assert resp.status_code == 401

def test_put_comment_forbidden(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "e", "name": "user"}
    resp = client.put("/api/comments/507f1f77bcf86cd799439011", json={"content": "C"})
    assert resp.status_code == 403

def test_put_comment_bad_request(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "e", "name": "admin"}
    resp = client.put("/api/comments/507f1f77bcf86cd799439011", json={"content": ""})
    assert resp.status_code == 400

def test_put_comment_success(monkeypatch, client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "e", "name": "moderator"}
    class C:
        def update_one(self, q, u): return None
    monkeypatch.setattr(app.mongo.db, "comments", C())
    resp = client.put("/api/comments/507f1f77bcf86cd799439011", json={"content": "Secret"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "redacted"}

# ----------------------------------------
# GET /api/article/<id>
# ----------------------------------------
def test_get_article_found(monkeypatch, client):
    data0 = {"response": {"docs": [{"_id": "X", "headline": {"main": "Hello"}}]}}
    class R:
        def __init__(self, j): self._j = j
        def json(self): return self._j
    def fake_get(url): return R(data0)
    monkeypatch.setattr(app, "requests", type("M", (), {"get": fake_get}))
    resp = client.get("/api/article/X")
    assert resp.status_code == 200
    assert resp.get_json()["headline"]["main"] == "Hello"

def test_get_article_not_found(monkeypatch, client):
    empty = {"response": {"docs": []}}
    monkeypatch.setattr(app, "requests", type("M", (), {"get": lambda url: type("R",(),{"json":lambda self: empty})()}))
    resp = client.get("/api/article/ID")
    assert resp.status_code == 404

def test_get_article_error(monkeypatch, client):
    def bad(url): raise Exception("fail")
    monkeypatch.setattr(app, "requests", type("M", (), {"get": bad}))
    resp = client.get("/api/article/Z")
    assert resp.status_code == 500
    assert "error" in resp.get_json()

# ----------------------------------------
# Static & Index serve_frontend
# ----------------------------------------
def test_serve_static(monkeypatch, client):
    monkeypatch.setattr(app.os.path, "exists", lambda p: True)
    monkeypatch.setattr(app, "send_from_directory", lambda folder, fn: f"{folder}/{fn}".encode())
    resp = client.get("/file.txt")
    assert resp.status_code == 200
    assert resp.data == b"static/file.txt"

def test_serve_index(monkeypatch, client):
    monkeypatch.setattr(app.os.path, "exists", lambda p: False)
    monkeypatch.setattr(app, "send_from_directory", lambda folder, fn: f"{folder}/{fn}".encode())
    resp = client.get("/random/path")
    assert resp.status_code == 200
    assert resp.data == b"templates/index.html"

# ----------------------------------------
# Exercise production‐only branches and __main__ block
# ----------------------------------------
def test_production_and_main_block(monkeypatch):
    # 1) Simulate production so we hit the PROD dotenv + secret_key-else branch
    monkeypatch.setenv("FLASK_ENV", "production")
    # Prevent actual .env loads
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *a, **k: None)
    # 2) Prevent server start
    monkeypatch.setattr(flask.Flask, "run", lambda self, *a, **k: None)
    # Re-execute module as __main__
    runpy.run_module("app", run_name="__main__", alter_sys=True)
