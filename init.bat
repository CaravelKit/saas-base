call venv\Scripts\activate.bat
call python -m pip install --upgrade pip
call pip install -r requirements.txt
call npm install
call flask dbinit -c
call npm run dev
call flask run