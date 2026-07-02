@echo off
title Launching JD Progress Dashboard...

:: 1. Initialize the Anaconda environment wrapper
call "C:\Users\Asus\anaconda3\Scripts\activate.bat"

:: 2. Activate your target Conda environment (replace 'base' if you use a custom environment name)
call conda activate base

:: 3. Change directory to where your script is saved
cd /d "C:\Users\Asus\Desktop\Python\JD"

:: 4. Boot up the Streamlit dashboard app
streamlit run app.py

pause