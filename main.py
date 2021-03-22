from scrapers.RedditScraper import RedditScraper
from sentiment_analysis import SentimentAnalysis
from entities.util.database_manager import DatabaseManager


def scrape_submission(submission_url):
	"""
	Receives a submission URL. Scrapes the data and inserts it into a submission, comment, and sentiment table in the
	database.

	:param submission_url:
	"""

	'''
	Scrape Data
	'''

	# Get submission dict
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

	# Completion notice
	print("Scrape Complete. See outputs.")

	'''
	Insert to Database
	'''

	# Create instance of database_manager
	database_manager = DatabaseManager()

	# Check if submission exists
	if database_manager.check_submission_exists(submission_dict):
		# Delete the submission and associated data if exists
		database_manager.delete_submission(submission_dict)

	# Insert new submission info into database
	new_submission = database_manager.insert_submission(submission_dict)

	# Insert comments if submission inserted successfully
	if new_submission is not None:
		database_manager.insert_comments(comments_dict, new_submission)
		database_manager.insert_sentiment(comments_dict)


# Login to Praw
reddit = RedditScraper()

'''
Read Job List
'''

# Read job_list.txt and scrape each url
with open('job/job_list.txt', "r") as job_list:
	urls = job_list.readlines()

for url in urls:

	scrape_submission(url)
