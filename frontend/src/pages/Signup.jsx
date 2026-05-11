import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { signup, login } from "../api"

function Signup() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    const data = await signup(email, password)
    if (data.id) {
      const loginData = await login(email, password)
      localStorage.setItem("token", loginData.access_token)
      navigate("/dashboard")
    } else {
      setError(data.detail || "Signup failed")
    }
  }

  return (
    <div className="container">
      <h2>Create account</h2>
      {error && <p style={{color:"red"}}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="email" placeholder="Email"
          value={email} onChange={e => setEmail(e.target.value)}
        />
        <input
          type="password" placeholder="Password"
          value={password} onChange={e => setPassword(e.target.value)}
        />
        <button type="submit">Sign up</button>
      </form>
      <p>Have an account? <Link to="/login">Login</Link></p>
    </div>
  )
}

export default Signup