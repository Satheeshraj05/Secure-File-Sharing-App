import axios from "axios"

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api/"

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor to add the token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token")
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

export const login = (username, password) => api.post("token/", { username, password })
export const register = (username, email, password) => api.post("users/", { username, email, password })
export const getFiles = () => api.get("files/")
export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append("file", file)
  
  try {
    const response = await api.post("files/", formData, {
      headers: {
        Accept: 'application/json',
      }
    })
    return response
  } catch (error) {
    console.error("Upload error details:", error.response?.data)
    throw error
  }
}
export const downloadFile = (fileId) => 
  api.get(`files/${fileId}/download/`, { 
    responseType: 'blob',
    headers: {
      'Accept': 'application/octet-stream'
    }
  })
export const shareFile = (fileId, userId, permission) =>
  api.post("file-shares/", { file: fileId, shared_with: userId, permission })
export const createShareableLink = (fileId) => api.post("shareable-links/", { file: fileId })

export default api

