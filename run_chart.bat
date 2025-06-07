@echo off
cd /d D:\finance

:: Activate virtual environment
call venv\Scripts\activate

:: Install required packages from requirements.txt (if not already installed)
pip install -r requirements.txt

:: Run the main script
python main.py --csv george.csv --output chart.html --since 2024-01-01

pause
