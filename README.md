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
* [Usage](#Usage)
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

Words

## Usage

Words about who can use our code

## Contributors

* [George Ciesinski](https://github.com/GeorgeCiesinski)
* [Saif Gorges](https://github.com/saif-gorges)