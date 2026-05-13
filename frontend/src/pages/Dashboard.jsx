import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import UploadForm from "../components/UploadForm"
import { getDocuments, analyzeDocument, deleteDocument } from "../api"

function Dashboard() {
  const [docs, setDocs] = useState([])
  const [questions, setQuestions] = useState({}) // Stores input text for each doc
  const [answers, setAnswers] = useState({})     // Stores AI responses for each doc
  const [loading, setLoading] = useState({})      // Tracks loading state per doc
  
  const navigate = useNavigate()
  const token = localStorage.getItem("token")

  async function fetchDocuments() {
    try {
      const data = await getDocuments(token)
      if (Array.isArray(data)) {
        setDocs(data)
      }
    } catch (error) {
      console.error(error)
    }
  }

  async function handleAnalyze(docId) {
    const userQuestion = questions[docId] || "Summarize this document"
    
    // Set loading for this specific document
    setLoading(prev => ({ ...prev, [docId]: true }))
    
    try {
      const result = await analyzeDocument(docId, token, userQuestion)
      // Store the answer specifically for this document ID
      setAnswers(prev => ({ ...prev, [docId]: result.analysis }))
    } catch (error) {
      console.error(error)
      alert("AI failed to respond. Please check your backend connection.")
    } finally {
      setLoading(prev => ({ ...prev, [docId]: false }))
    }
  }

  async function handleDelete(docId) {
    if (!confirm("Are you sure you want to delete this document?")) return
    try {
      await deleteDocument(docId, token)
      fetchDocuments()
    } catch (error) {
      console.error(error)
      alert("Delete failed")
    }
  }

  useEffect(() => {
    if (!token) {
      navigate("/login")
      return
    }
    fetchDocuments()
  }, [])

  function logout() {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <div className="container" style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px"
        }}
      >
        <h2>My Documents</h2>
        <button onClick={logout} style={{ padding: "8px 16px" }}>Logout</button>
      </div>

      <UploadForm onUploadSuccess={fetchDocuments} />

      <div style={{ marginTop: "20px" }}>
        {docs.length === 0 && <p>No documents yet. Upload one to start!</p>}

        {docs.map((doc) => (
          <div
            key={doc.id}
            style={{
              border: "1px solid #ddd",
              padding: "20px",
              marginBottom: "15px",
              borderRadius: "12px",
              backgroundColor: "#fff",
              boxShadow: "0 2px 4px rgba(0,0,0,0.05)"
            }}
          >
            <h3 style={{ marginTop: 0 }}>{doc.filename}</h3>
            {doc.content && (
              <p style={{ fontSize: "0.9rem", color: "#666", backgroundColor: "#f9f9f9", padding: "10px", borderRadius: "5px" }}>
                <strong>Preview:</strong> {doc.content.substring(0, 200)}...
              </p>
            )}

            {/* --- AI QUESTION INPUT --- */}
            <div style={{ marginTop: "15px", display: "flex", gap: "10px" }}>
              <input
                type="text"
                placeholder="Ask a question about this file..."
                value={questions[doc.id] || ""}
                onChange={(e) => setQuestions({ ...questions, [doc.id]: e.target.value })}
                style={{
                  flex: 1,
                  padding: "10px",
                  borderRadius: "6px",
                  border: "1px solid #ccc"
                }}
              />
              <button 
                onClick={() => handleAnalyze(doc.id)}
                disabled={loading[doc.id]}
                style={{ 
                  padding: "10px 20px", 
                  backgroundColor: "#007bff", 
                  color: "white", 
                  border: "none", 
                  borderRadius: "6px",
                  cursor: "pointer"
                }}
              >
                {loading[doc.id] ? "Thinking..." : "Ask AI"}
              </button>
            </div>

            {/* --- AI RESPONSE DISPLAY --- */}
            {answers[doc.id] && (
              <div style={{ 
                marginTop: "15px", 
                padding: "15px", 
                backgroundColor: "#eef6ff", 
                borderRadius: "8px",
                borderLeft: "5px solid #007bff",
                lineHeight: "1.5"
              }}>
                <strong style={{ display: "block", marginBottom: "5px" }}>DocuMind AI:</strong> 
                {answers[doc.id]}
              </div>
            )}

            <div style={{ marginTop: "20px", borderTop: "1px solid #eee", paddingTop: "10px" }}>
              <button
                onClick={() => handleDelete(doc.id)}
                style={{ 
                  color: "#d9534f", 
                  background: "none", 
                  border: "none", 
                  cursor: "pointer", 
                  fontWeight: "bold" 
                }}
              >
                Delete Document
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dashboard