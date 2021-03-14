from scrapers.RedditScraper import RedditScraper
from sentiment_analysis import SentimentAnalysis
from entities.util.database_manager import DatabaseManager


# Login to Praw
reddit = RedditScraper()

'''
Scrape Data
'''

# Get submission dict
submission_url = input('Enter the post url: ')
submission_dict = reddit.extract_post_data(submission_url=submission_url)

# Get list of comments_dicts
submission_object = submission_dict.get('submission_object')
comments_dict = reddit.extract_post_comments_data(submission_object)

'''
Analyze Sentiment
'''

# Call sentimentanalysis to analyze the comments and append the dicts
SentimentAnalysis.list_parser(comments_dict)

'''
Text Output for Debugging
'''

# Output submission data
with open('output/submission_dict.txt', "w+") as text_file:
	text_file.write(str(submission_dict))

# Output comment data
with open('output/comments_dict.txt', "w+") as text_file:
	text_file.write(str(comments_dict))

# Temporarily output data for debugging
# Todo: Update to remove once SQLAlchemy is working
print("Scrape Complete. See outputs.")

'''
Insert to Database
'''

dm = DatabaseManager()

new_submission = dm.insert_submission(submission_dict)

# Insert comments if submission inserted successfully
if new_submission is not None:
	dm.insert_comments(comments_dict, new_submission)
