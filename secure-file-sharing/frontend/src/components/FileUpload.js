import React, { useState } from "react"
import { useDispatch } from "react-redux"
import { addFile } from "../redux/fileSlice"
import { uploadFile } from "../services/api"
import { Button, Typography, LinearProgress, Snackbar } from "@mui/material"
import { CloudUpload } from "@mui/icons-material"

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState("")
  const dispatch = useDispatch()

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0])
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file to upload.")
      return
    }

    setUploading(true)
    try {
      console.log("Selected file:", selectedFile) // Debug log
      
      const response = await uploadFile(selectedFile)
      if (response?.data) {
        dispatch(addFile(response.data))
        setSelectedFile(null)
        setError("File uploaded successfully")
      }
    } catch (error) {
      console.error("File upload failed:", error.response?.data || error)
      setError(
        error.response?.data?.detail ||
          error.response?.data?.file ||
          error.message ||
          "File upload failed. Please try again."
      )
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <input accept="*/*" style={{ display: "none" }} id="raised-button-file" type="file" onChange={handleFileSelect} />
      <label htmlFor="raised-button-file">
        <Button variant="contained" component="span" startIcon={<CloudUpload />}>
          Select File
        </Button>
      </label>
      {selectedFile && (
        <Typography variant="body2" style={{ marginTop: 10 }}>
          Selected file: {selectedFile.name}
        </Typography>
      )}
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={!selectedFile || uploading}
        style={{ marginTop: 10 }}
      >
        Upload
      </Button>
      {uploading && <LinearProgress style={{ marginTop: 10 }} />}
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError("")} message={error} />
    </div>
  )
}

export default FileUpload

