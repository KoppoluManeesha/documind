import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { getDocuments } from "../api"

function Dashboard() {
  const [docs, setDocs] = useState([])
  const navigate = useNavigate()
  const token = localStorage.getItem("token")

  useEffect(() => {
    if (!token) {
      navigate("/login")
      return
    }
    getDocuments(token).then(data => {
      if (Array.isArray(data)) setDocs(data)
    })
  }, [])

  function logout() {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <div className="container">
      <div style={{display:"flex", justifyContent:"space-between"}}>
        <h2>My Documents</h2>
        <button onClick={logout}>Logout</button>
      </div>
      {docs.length === 0 && <p>No documents yet.</p>}
      {docs.map(doc => (
        <div key={doc.id} style={{border:"1px solid #ddd", padding:"12px", marginBottom:"8px", borderRadius:"8px"}}>
          <h3>{doc.title}</h3>
          <p>{doc.content}</p>
        </div>
      ))}
    </div>
  )
}

export default Dashboard