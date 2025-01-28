import React, { useEffect, useState } from "react"
import { useSelector, useDispatch } from "react-redux"
import { setFiles, removeFile } from "../redux/fileSlice"
import { getFiles, downloadFile } from "../services/api"
import { List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Typography, Snackbar } from "@mui/material"
import { GetApp, Delete, Share } from "@mui/icons-material"

const FileList = () => {
  const files = useSelector((state) => state.file.files)
  const dispatch = useDispatch()
  const [error, setError] = useState("")

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await getFiles()
        dispatch(setFiles(response.data))
      } catch (error) {
        console.error("Failed to fetch files:", error)
        setError("Failed to fetch files. Please try again.")
      }
    }
    fetchFiles()
  }, [dispatch])

  const handleDownload = async (fileId) => {
    try {
      const response = await downloadFile(fileId)
      
      // Get filename from Content-Disposition header if available
      const contentDisposition = response.headers?.['content-disposition']
      let filename = 'downloaded_file'
      if (contentDisposition) {
        const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition)
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '')
        }
      }
  
      // Create blob URL and trigger download
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      
      // Cleanup
      window.URL.revokeObjectURL(url)
      document.body.removeChild(link)
    } catch (error) {
      console.error("Download failed:", error)
      setError(error.response?.data?.error || "Failed to download file. Please try again.")
    }
  }
  

  const handleDelete = async (fileId) => {
    try {
      await removeFile(fileId)
      dispatch(removeFile(fileId))
    } catch (error) {
      console.error("Failed to delete file:", error)
      setError("Failed to delete file. Please try again.")
    }
  }

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Your Files
      </Typography>
      <List>
        {files.map((file) => (
          <ListItem key={file.id}>
            <ListItemText
              primary={file.name}
              secondary={`Uploaded on: ${new Date(file.uploaded_at).toLocaleString()}`}
            />
            <ListItemSecondaryAction>
              <IconButton edge="end" aria-label="download" onClick={() => handleDownload(file.id)}>
                <GetApp />
              </IconButton>
              <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(file.id)}>
                <Delete />
              </IconButton>
              <IconButton edge="end" aria-label="share">
                <Share />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError("")} message={error} />
    </div>
  )
}

export default FileList
