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


### Commandline

    Python script/Scraper.py SUBREDDIT -m MINIMUM -s /path/to/save_location -l

    SUBREDDIT: Subreddit to scrape

    -m: Minimum number of records to collect before quitting the script (required. Ex: 10000)

    -s: path to your save location (if load option is used, location of the folder of your save files)

    -l: Load flag to continue scraping from earlier (if used, save location is required)

Example usage:

    Python script/Scraper.py Gaming -m 10000 -s /data/raw


### GUI

You are also free to run electron package (More instructions coming soon, along with a fully packaged version of the GUI).

If you want to try the electron app:

- Make sure to download electron and node.js
- Run using npm start .

