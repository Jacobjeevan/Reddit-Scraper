# Reddit Scraper

This is a Python Scraper script built on top of PRAW script. This script is used to collect data for the Reddit Gild Predictor project.

# Running:

## Step 1: Clone from Github:

> git clone https://github.com/Jacobjeevan/Reddit-Scraper

## Step 2: Create Reddit App and modify PRAW file

Create a Reddit account to use for scraping.
Create a Reddit developer app to acquire client ID and secret keys.
Modify the praw.ini file with relevant details (Client ID, secret key reddit username, password)

## Step 3: Run the Script

> Python Scraper.py -c CHECKPOINT -m MINIMUM

**CHECKPOINT**: Use checkpoint to decide save points (Ex: Save records every 10k records. Default: 10k)
**MINIMUM**: Minimum number of records to collect before quitting the script. Default: 200k).




