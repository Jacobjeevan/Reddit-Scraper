# Reddit Scraper

This is a Python Scraper script built on top of PRAW script. This script was used to collect data for the Reddit Gild Predictor project.

# Running:

## Step 1: Clone from Github:

> git clone https://github.com/Jacobjeevan/Reddit-Scraper

## Step 2: Create Reddit App and modify PRAW file

- Login to your reddit account (or create one)
- Navigate to reddit.com/prefs/apps
- Click on create another app
- Give it a name, description and other details. You can use "http://localhost:8080" for the url. Use the "script" option.
- Grab the secret key and Client ID for later use
- Install the dependencies (pip install -r requirements.txt)
- Modify the default praw.ini file (Client ID, secret key, reddit username and password associated with the app)

## Step 3: Run the Script

> Python Scraper.py -c CHECKPOINT -m MINIMUM

**CHECKPOINT**: Use checkpoint to decide save points (Ex: Save records every 10k records. Default: 10k)

**MINIMUM**: Minimum number of records to collect before quitting the script. Default: 200k).




