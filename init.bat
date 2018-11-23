call venv\Scripts\activate.bat
call python -m pip install --upgrade pip
call pip install -r requirements.txt
call npm install
call flask dbcreate REM use flask dbupdate for just updating existing database
call npm run dev
call flask run