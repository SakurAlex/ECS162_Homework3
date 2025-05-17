const BASE = import.meta.env.VITE_BASE_URL || "";

export const fetchArticles = () =>
  fetch(`${BASE}/api/ucdavis-news`, { credentials:"include" }).then(r=>r.json());

export const fetchComments = (aid:string) =>
  fetch(`${BASE}/api/comments?article_id=${aid}`, { credentials:"include" }).then(r=>r.json());

export const postComment = (aid:string, content:string) =>
  fetch(`${BASE}/api/comments`, {
    method:"POST", credentials:"include",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({article_id:aid, content})
  }).then(r=>r.json());

export const deleteComment = (cid:string) =>
  fetch(`${BASE}/api/comments/${cid}`, {
    method:"DELETE", credentials:"include"
  });
