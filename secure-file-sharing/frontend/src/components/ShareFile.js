import React, { useState } from "react"
import { createShareableLink } from "../services/api"
import { TextField, Button, Typography, Snackbar } from "@material-ui/core"

const ShareFile = ({ fileId }) => {
  const [shareableLink, setShareableLink] = useState("")
  const [error, setError] = useState("")

  const handleCreateLink = async () => {
    try {
      const response = await createShareableLink(fileId)
      setShareableLink(response.data.token)
    } catch (error) {
      console.error("Failed to create shareable link:", error)
      setError(error.response?.data?.error || "Failed to create shareable link. Please try again.")
    }
  }

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Share File
      </Typography>
      <Button variant="contained" color="primary" onClick={handleCreateLink}>
        Create Shareable Link
      </Button>
      {shareableLink && (
        <Typography variant="body1" style={{ marginTop: 10 }}>
          Shareable Link: {shareableLink}
        </Typography>
      )}
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError("")} message={error} />
    </div>
  )
}

export default ShareFile

