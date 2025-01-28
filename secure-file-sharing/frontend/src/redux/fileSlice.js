import { createSlice } from "@reduxjs/toolkit"

const fileSlice = createSlice({
  name: "file",
  initialState: {
    files: [],
  },
  reducers: {
    setFiles: (state, action) => {
      state.files = action.payload
    },
    addFile: (state, action) => {
      state.files.push(action.payload)
    },
    removeFile: (state, action) => {
      state.files = state.files.filter((file) => file.id !== action.payload)
    },
  },
})

export const { setFiles, addFile, removeFile } = fileSlice.actions

export default fileSlice.reducer

