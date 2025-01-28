import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import FileUpload from './FileUpload';
import FileList from './FileList';

const Dashboard = () => {
  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <FileUpload />
        <Box mt={4}>
          <FileList />
        </Box>
      </Box>
    </Container>
  );
};

export default Dashboard;
