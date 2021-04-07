# social-media-analysis

Social-media-analysis is a project created by Saif Gorges and George Ciesinski which
analyzes Reddit submissions and comments to analyze the overall sentiment of the
responses to the submission. This project was intended as a learning device for the
two of us to improve our programming knowledge in a few different areas, such as
sentiment analysis, PostgreSQL and SQLAlchemy, data scraping, and collaboration. 

## Table of Contents

* [Overview](#Overview)
* [Data Analysis](#Data Analysis)
* [Installation](#Installation)
* [How to use social-media-analysis](#How to use social-media-analysis)
* [Contributors](#Contributors)

## Overview

Social-Media-Analysis is composed of two parts. The first part is a Reddit bot made using
the Reddit API [PRAW](https://pypi.org/project/praw/). The bot scrapes submission and comment 
data from a list of submission URLs and populates the data into a dictionary. The data is then 
analyzed by the TextBlob library to determine the sentiment values and update the dictionary. 
Finally, the data form the dictionary is inserted into a [PostgreSQL](https://www.postgresql.org) 
database using [SQLAlchemy](https://www.sqlalchemy.org). 

The second part is a data plotter which creates dataframes and utilizes Matplotlib to
plot the data into different kinds of graphs. 

The raw data from the analysis is stored in the database and can be retreived at a later
date for further analysis.

## Data Analysis

The objective of this project is to collect sufficient data from the submission and comments
to determine several areas of interest:

* Overall sentiment of submission replies
* The number of replies and upvotes the replies have
* The change in the overall sentiment of comments over time
* The overall distribution of upvotes over comments with different levels of sentiment

This data can provide meaningful insights into how different communities feel about certain
topics, events, or social media posts.

## Installation

1. Clone this repository to a local directory.
2. Install `requirements.txt` for Windows or `requirements-binary.txt` for Mac / Linux. Note: The
   requirements.txt file contains psycopg2 while the requirements-binary.txt file contains psycopg2-binary.
3. Create a `connection_string.txt` file in the `config` directory. This file requires a database
   connection string in the below format.
   
```
postgres://username:password@connection_url/database_name
```

4. Create a `login.ini` file in the `config` directory. This file requires PRAW login
   information in the below format. To get this information, you must first register
   a Reddit bot account.
   
```
[login]
client_id = [your client id]
client_secret = [your client_secret]
password = [your password]
user_agent = [your user_agent]
username = [your username]
```

Once you have completed these steps, the bot is ready to be ran.

## How to use social-media-analysis

### Instructions

1. Open the scrape_job_list.txt file. Enter the URL of each submission to be scraped on separate lines.
2. Run the `data_collector.py` file. This script will populate the database with the submission data and
   update the `job/plot_job_list.txt` file with the submission ids. This process can take a long time depending
   on the number of comments, so be patient during this process.
3. Run the `data_plotter.py` file. This will look up the submissions in the `job/plot_job_list.txt` file and
   will generate folders in the `output/graphs/` directory named after the submission ids. These folders will
   contain all the generated graphs for the submissions.

### Job Lists and Job Failure

**social-media-analysis** uses the `scrape_job_list.txt` and `plot_job_list.txt` files to determine which jobs
to run. Once the job is ran, it is removed from the list. 

Sometimes jobs can fail for a number of different reasons. There might be an error in the URL, or the network connection
may be down. **social-media-analysis** only removes the jobs from the job list if data collection or
plotting is successful. In the event of failure, you should find the failed job in the job list.

### Logging

**social-media-analysis** takes logs during the data collection and plotting process. In the event of job failure, you can 
find these logs in the `logs/` directory within a file called `social-media-analysis.log`. This will most
likely contain the error that was experienced, and which job caused the error. 

## Contributors

* [George Ciesinski](https://github.com/GeorgeCiesinski)
* [Saif Gorges](https://github.com/saif-gorges)