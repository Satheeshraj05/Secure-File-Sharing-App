import React, { useState } from "react"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { login } from "../services/api"
import { setUser, setToken } from "../redux/authSlice"
import { TextField, Button, Typography, Container, Snackbar } from "@mui/material"

const Login = () => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      console.log("Attempting login...")
      const response = await login(username, password)
      console.log("Login response:", response)
      dispatch(setToken(response.data.access))
      dispatch(setUser(response.data.user))
      navigate("/dashboard")
    } catch (error) {
      console.error("Login failed:", error)
      console.error("Error details:", error.response?.data || error.message)
      setError(error.response?.data?.detail || "Login failed. Please try again.")
    }
  }

  return (
    <Container maxWidth="xs">
      <Typography variant="h4" align="center" gutterBottom>
        Login
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit" fullWidth variant="contained" color="primary">
          Login
        </Button>
      </form>
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError("")} message={error} />
    </Container>
  )
}

export default Login

