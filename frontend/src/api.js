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
export const analyzeDocument = async (docId, token, question) => {
  // Updated URL to match {BF44F80A-A501-4998-9CB2-B87DDE620CAF}.png
  const response = await fetch(`${BASE}/analyze/${docId}`, { 
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ prompt: question }), 
  });

  if (!response.ok) {
    const errorBody = await response.json();
    console.error("AI Error:", errorBody);
    throw new Error("Failed to analyze");
  }
  return response.json();
};
export async function deleteDocument(docId, token) {
  const res = await fetch(`${BASE}/documents/${docId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return res.json()
}