const BASE = "http://localhost:8000"

export async function signup(email, password) {
  const res = await fetch(`${BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
  return res.json()
}

export async function login(email, password) {
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
  return res.json()
}

export async function getDocuments(token) {
  const res = await fetch(`${BASE}/documents`, {
    headers: { "Authorization": `Bearer ${token}` },
  })
  return res.json()
}

export async function createDocument(token, title, content) {
  const res = await fetch(`${BASE}/documents`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, content }),
  })
  return res.json()
}