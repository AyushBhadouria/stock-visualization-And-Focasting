@echo off
echo Setting up Stock Platform...

echo.
echo 1. Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
echo Backend setup complete!

echo.
echo 2. Setting up Frontend...
cd ..\frontend
npm install
echo Frontend setup complete!

echo.
echo 3. Setup complete!
echo.
echo To start the application:
echo 1. Start backend: cd backend && venv\Scripts\activate && python main.py
echo 2. Start frontend: cd frontend && npm start
echo.
echo Or use Docker: docker-compose up
echo.
echo Don't forget to:
echo - Set up PostgreSQL database
echo - Configure API keys in backend\.env
echo - Update database connection string

pause