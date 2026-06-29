# ZERO TECH SETUP GUIDE - tozy.ai

## STEP 1: Install PostgreSQL

WHERE:
Web browser

PASTE:
https://www.postgresql.org/download/windows/

EXPECT:
Download page opens

WHERE:
Web browser

PASTE:
Click "Download" button

EXPECT:
Installer downloads

WHERE:
Windows

PASTE:
Run the installer

EXPECT:
Setup wizard opens

WHERE:
Setup wizard

PASTE:
Click "Next" through all screens

EXPECT:
Password prompt appears

WHERE:
Password prompt

PASTE:
Enter password (REMEMBER THIS PASSWORD)

EXPECT:
Installation completes

WHERE:
Windows

PASTE:
Restart computer

EXPECT:
Computer restarts

## STEP 2: Install Python

WHERE:
Web browser

PASTE:
https://www.python.org/downloads/

EXPECT:
Download page opens

WHERE:
Web browser

PASTE:
Click "Download Python 3.12.x"

EXPECT:
Installer downloads

WHERE:
Windows

PASTE:
Run the installer

EXPECT:
Setup wizard opens

WHERE:
Setup wizard

PASTE:
Check the box "Add Python to PATH"

EXPECT:
Box is checked

WHERE:
Setup wizard

PASTE:
Click "Install Now"

EXPECT:
Installation completes

WHERE:
Setup wizard

PASTE:
Click "Close"

EXPECT:
Window closes

## STEP 3: Install Node.js

WHERE:
Web browser

PASTE:
https://nodejs.org/

EXPECT:
Download page opens

WHERE:
Web browser

PASTE:
Click "Download Node.js (LTS)"

EXPECT:
Installer downloads

WHERE:
Windows

PASTE:
Run the installer

EXPECT:
Setup wizard opens

WHERE:
Setup wizard

PASTE:
Click "Next" through all screens

EXPECT:
Install button appears

WHERE:
Setup wizard

PASTE:
Click "Install"

EXPECT:
Installation completes

WHERE:
Setup wizard

PASTE:
Click "Finish"

EXPECT:
Window closes

## STEP 4: Install Git

WHERE:
Web browser

PASTE:
https://git-scm.com/download/win

EXPECT:
Download page opens

WHERE:
Web browser

PASTE:
Click "Download for Windows"

EXPECT:
Installer downloads

WHERE:
Windows

PASTE:
Run the installer

EXPECT:
Setup wizard opens

WHERE:
Setup wizard

PASTE:
Click "Next" through all screens

EXPECT:
Install button appears

WHERE:
Setup wizard

PASTE:
Click "Install"

EXPECT:
Installation completes

WHERE:
Setup wizard

PASTE:
Click "Finish"

EXPECT:
Window closes

## STEP 5: Open Command Prompt

WHERE:
Windows

PASTE:
Press Windows key

EXPECT:
Start menu opens

WHERE:
Start menu

PASTE:
Type "cmd"

EXPECT:
Command Prompt appears

WHERE:
Start menu

PASTE:
Press Enter

EXPECT:
Black window opens

## STEP 6: Go to Project Folder

WHERE:
Command Prompt

PASTE:
cd C:\Users\ac\CascadeProjects\indian-trading-platform

EXPECT:
Path changes to project folder

## STEP 7: Open SQL Shell

WHERE:
Windows

PASTE:
Press Windows key

EXPECT:
Start menu opens

WHERE:
Start menu

PASTE:
Type "SQL Shell"

EXPECT:
SQL Shell (psql) appears

WHERE:
Start menu

PASTE:
Press Enter

EXPECT:
SQL Shell window opens

## STEP 8: Connect to PostgreSQL

WHERE:
SQL Shell

PASTE:
Press Enter (Server)

EXPECT:
Prompts for Database

WHERE:
SQL Shell

PASTE:
Press Enter (Database)

EXPECT:
Prompts for Port

WHERE:
SQL Shell

PASTE:
Press Enter (Port)

EXPECT:
Prompts for Username

WHERE:
SQL Shell

PASTE:
Enter postgres

EXPECT:
Prompts for Password

WHERE:
SQL Shell

PASTE:
Enter your PostgreSQL password

EXPECT:
Connected to postgres

## STEP 9: Create Database

WHERE:
SQL Shell

PASTE:
CREATE DATABASE trading_platform;

EXPECT:
CREATE DATABASE

## STEP 10: Load Database Schema

WHERE:
SQL Shell

PASTE:
\i C:\Users\ac\CascadeProjects\indian-trading-platform\database\schema.sql

EXPECT:
Schema loads successfully

WHERE:
SQL Shell

PASTE:
\q

EXPECT:
SQL Shell closes

## STEP 11: Go to Backend Folder

WHERE:
Command Prompt

PASTE:
cd backend

EXPECT:
Path changes to backend folder

## STEP 12: Create Python Virtual Environment

WHERE:
Command Prompt

PASTE:
python -m venv venv

EXPECT:
venv folder created

## STEP 13: Activate Virtual Environment

WHERE:
Command Prompt

PASTE:
venv\Scripts\activate

EXPECT:
(venv) appears at start of line

## STEP 14: Install Python Dependencies

WHERE:
Command Prompt

PASTE:
pip install -r requirements.txt

EXPECT:
Installation completes (2-5 minutes)

## STEP 15: Create Environment File

WHERE:
Command Prompt

PASTE:
copy .env.example .env

EXPECT:
.env file created

## STEP 16: Edit Environment File

WHERE:
Command Prompt

PASTE:
notepad .env

EXPECT:
Notepad opens with .env file

WHERE:
Notepad

PASTE:
Replace your-postgresql-password with your actual PostgreSQL password

EXPECT:
Password is updated

WHERE:
Notepad

PASTE:
Replace your-secret-key with a strong random string

EXPECT:
Secret key is updated

WHERE:
Notepad

PASTE:
Replace your-jwt-secret-key with a different strong random string

EXPECT:
JWT secret is updated

WHERE:
Notepad

PASTE:
Ctrl+S

EXPECT:
File saves

WHERE:
Notepad

PASTE:
Close notepad

EXPECT:
Window closes

## STEP 17: Start Backend

WHERE:
Command Prompt

PASTE:
python app.py

EXPECT:
Server starts on http://localhost:5000

## STEP 18: Open NEW Command Prompt

WHERE:
Windows

PASTE:
Press Windows key

EXPECT:
Start menu opens

WHERE:
Start menu

PASTE:
Type "cmd"

EXPECT:
Command Prompt appears

WHERE:
Start menu

PASTE:
Press Enter

EXPECT:
Black window opens

## STEP 19: Go to Frontend Folder

WHERE:
Command Prompt

PASTE:
cd C:\Users\ac\CascadeProjects\indian-trading-platform\frontend

EXPECT:
Path changes to frontend folder

## STEP 20: Install Frontend Dependencies

WHERE:
Command Prompt

PASTE:
npm install

EXPECT:
Installation completes (5-10 minutes)

## STEP 21: Create Frontend Environment File

WHERE:
Command Prompt

PASTE:
echo NEXT_PUBLIC_API_URL=http://localhost:5000/api > .env.local

EXPECT:
.env.local file created

## STEP 22: Start Frontend

WHERE:
Command Prompt

PASTE:
npm run dev

EXPECT:
Server starts on http://localhost:3000

## STEP 23: Test Backend

WHERE:
Web browser

PASTE:
http://localhost:5000/api/health

EXPECT:
{"status":"healthy","service":"tozy.ai-backend",...}

## STEP 24: Test Frontend

WHERE:
Web browser

PASTE:
http://localhost:3000

EXPECT:
tozy.ai landing page appears

## STEP 25: Close Both Windows

WHERE:
Backend command window

PASTE:
Close window

EXPECT:
Window closes

WHERE:
Frontend command window

PASTE:
Close window

EXPECT:
Window closes

## STEP 26: Initialize Git

WHERE:
Command Prompt

PASTE:
cd C:\Users\ac\CascadeProjects\indian-trading-platform

EXPECT:
Path changes to project folder

WHERE:
Command Prompt

PASTE:
git init

EXPECT:
Initialized empty Git repository message

## STEP 27: Add Remote Repository

WHERE:
Command Prompt

PASTE:
git remote add origin https://github.com/rahulxproject/tozy.git

EXPECT:
No error message

## STEP 28: Add All Files

WHERE:
Command Prompt

PASTE:
git add .

EXPECT:
No error message

## STEP 29: Commit Files

WHERE:
Command Prompt

PASTE:
git commit -m "Initial commit"

EXPECT:
Commit message appears

## STEP 30: Push to GitHub

WHERE:
Command Prompt

PASTE:
git push -u origin main

EXPECT:
Files upload to GitHub

## ALTERNATIVE: DOCKER SETUP (RECOMMENDED FOR WINDOWS)

This method avoids Python build issues on Windows by using Docker containers.

### Prerequisite: Install Docker Desktop

WHERE:
Web browser

PASTE:
https://www.docker.com/products/docker-desktop/

EXPECT:
Download page opens

WHERE:
Web browser

PASTE:
Download Docker Desktop for Windows

EXPECT:
Installer downloads

WHERE:
Windows

PASTE:
Run the installer

EXPECT:
Docker Desktop installs

WHERE:
Windows

PASTE:
Restart computer

EXPECT:
Computer restarts

### Docker Setup Steps

WHERE:
Command Prompt

PASTE:
cd C:\Users\ac\CascadeProjects\indian-trading-platform

EXPECT:
Path changes to project folder

WHERE:
Command Prompt

PASTE:
docker-compose up -d

EXPECT:
PostgreSQL and backend containers start

WHERE:
Command Prompt

PASTE:
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE trading_platform;"

EXPECT:
Database created

WHERE:
Command Prompt

PASTE:
docker-compose exec -T postgres psql -U postgres -d trading_platform < database/schema.sql

EXPECT:
Schema loads successfully

WHERE:
Command Prompt

PASTE:
docker-compose ps

EXPECT:
Both services show as "Up"

### To Stop Docker Services

WHERE:
Command Prompt

PASTE:
docker-compose down

EXPECT:
Containers stop

### To Start Docker Services Again

WHERE:
Command Prompt

PASTE:
docker-compose up -d

EXPECT:
Containers start

## TO RUN AGAIN LATER:

**Backend:**

WHERE:
Command Prompt

PASTE:
cd C:\Users\ac\CascadeProjects\indian-trading-platform\backend

EXPECT:
Path changes to backend folder

WHERE:
Command Prompt

PASTE:
venv\Scripts\activate

EXPECT:
(venv) appears at start of line

WHERE:
Command Prompt

PASTE:
python app.py

EXPECT:
Server starts on http://localhost:5000

**Frontend:**

WHERE:
NEW Command Prompt

PASTE:
cd C:\Users\ac\CascadeProjects\indian-trading-platform\frontend

EXPECT:
Path changes to frontend folder

WHERE:
Command Prompt

PASTE:
npm run dev

EXPECT:
Server starts on http://localhost:3000
