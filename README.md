# Expense Management System

This project is an expense management system that consists of a Streamlit frontend application and a FastApi backend server

## Project Structure

**frontend/**: Contains the streamlit application code.

**backend/**: Contains the FastApi Backend server code.

**tests/**: contains the test cases for both frontend and backend.

**requirements.txt/**: List the required python packages.

**README.md/**: Provides an overview and instruction for the project.

## Setup Instructions

## 🚀 Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/expense-management-system
   cd expense-management-system

2. **Install dependencies**  
   ```commandline
   pip install -r requirements.txt


3. **Run the FastAPI server**  
   ```commandline
   uvicorn server.server:app --reload

4. **Run the Streamlit app**  
   ```commandline
   streamlit run frontend/app.py

