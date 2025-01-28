import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import fileReducer from './fileSlice';

export default configureStore({
  reducer: {
    auth: authReducer,
    file: fileReducer,
  },
});