import { useState, useEffect } from "react"
import "./App.css"

function App() {
  const [message, setMessage] = useState("")

  useEffect(() => {
    fetch("http://localhost:8000/")
      .then(res => res.json())
      .then(data => setMessage(data.message))
  }, [])

  return (
    <div className="container">
      <h1>DocuMind 🧠</h1>
      <p>{message || "Connecting to backend..."}</p>
    </div>
  )
}

export default App