# Secure File Sharing Project

## Project Overview
This project is a **Secure File Sharing** application built with **React.js** for the frontend and **Django REST Framework** for the backend. It allows users to upload, download, and share files securely.

---

## Prerequisites
Ensure you have the following installed:
- **Node.js** (Download from [Node.js](https://nodejs.org/))
- **Python 3.8+** (Download from [Python.org](https://www.python.org/downloads/))
- **Git** (Download from [Git](https://git-scm.com/downloads))

---

## Getting Started
### Clone the Repository
```sh
 git clone https://github.com/Satheeshraj05/Secure-File-Sharing.git
 cd Secure-File-Sharing
```

---

## Frontend Setup
### 1. Create a New React App
```sh
npx create-react-app frontend
cd frontend
```

### 2. Install Dependencies
```sh
npm install axios redux react-redux @reduxjs/toolkit react-router-dom @material-ui/core @material-ui/icons
```

### 3. Start the Development Server
```sh
npm start
```
This will launch the React application at `http://localhost:3000/`.

---

## Backend Setup
### 1. Install Python and Dependencies
If you haven't already installed Python, download it from [here](https://www.python.org/downloads/).

### 2. Install Django and Other Dependencies
Create a `requirements.txt` file in the `backend` directory with the following content:
```plaintext
Django==3.2.10
djangorestframework==3.12.4
djangorestframework-simplejwt==4.8.0
django-cors-headers==3.10.0
cryptography==3.4.7
pyotp==2.6.0
```
Then, install dependencies:
```sh
pip install -r requirements.txt
```

### 3. Create a New Django Project
```sh
django-admin startproject secure_file_sharing
cd secure_file_sharing
```

### 4. Create a New Django App
```sh
python manage.py startapp file_sharing
```

### 5. Run Migrations and Start Backend Server
```sh
python manage.py migrate
python manage.py runserver
```
The Django server will run at `http://127.0.0.1:8000/`.

---

## API Endpoints
| Endpoint              | Method | Description         |
|----------------------|--------|---------------------|
| `/api/register/`    | POST   | Register new user  |
| `/api/login/`       | POST   | User login         |
| `/api/upload/`      | POST   | Upload file        |
| `/api/files/`       | GET    | Fetch all files    |
| `/api/download/`    | GET    | Download file      |

---

## Folder Structure
```
Secure-File-Sharing/
│── backend/
│   ├── secure_file_sharing/
│   ├── file_sharing/
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── redux/
│── README.md
```

---

## Contributing
If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m "Add new feature"`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

Login Credentials

Backend & Frontend

Username: user1

Password: Qwertyuiop@123

---

## Contact
For any questions or issues, reach out to **Satheesh R**:
- **Email:** [satheeshraj333@gmail.com](mailto:satheeshraj333@gmail.com)
- **LinkedIn:** [Satheesh Raj](https://www.linkedin.com/in/satheesh-raj/)
- **GitHub:** [Satheeshraj05](https://github.com/Satheeshraj05/)
