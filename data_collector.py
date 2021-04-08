from scrapers.RedditScraper import RedditScraper
from sentiment_analysis import SentimentAnalysis
from entities.util.database_manager import DatabaseManager
from logs.Logger import base_logger

logger = base_logger.getChild(__name__)


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
	Exit if no comments were extracted from the submission
	'''

	if not len(comments_dict.get('data')) > 0:
		logger.info('Data extraction yielded zero comments. Aborting sentiment analysis and database insertion.')
		return

	'''
	Analyze Sentiment
	'''

	# Call sentimentanalysis to analyze the comments and append the dicts
	SentimentAnalysis.list_parser(comments_dict)

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

	# Returns submission_id
	return submission_dict.get('id')


def execute_job_list():

	# Instantiating empty lists for failed jobs
	new_urls = []
	completed_submission_ids = []

	logger.info(f'Reading job/{scrape_list_directory}.')

	# Read scrape_job_list.txt and scrape each url
	with open(scrape_list_directory, "r") as scrape_job_list:
		urls = scrape_job_list.read().splitlines()

	logger.info(f'Found {len(urls)} jobs.')

	# Iterate through list of submissions and scrape each one
	for url in urls:

		logger.info(f'Scraping url: {url}')

		try:
			submission_id = scrape_submission(url)  # Scrape the submission, return submission id
			completed_submission_ids.append(submission_id)  # Update completed_submission_ids with submission_id
			logger.info('Removing url from job list.')
		except Exception as e:
			logger.error('Unexpected error occurred. Aborted scraping url.')
			logger.error(e)
			# Append url to new_urls
			new_urls.append(url)

	return new_urls, completed_submission_ids


def update_job_lists(new_urls, completed_submission_ids):

	with open(scrape_list_directory, 'w') as scrape_job_list:

		if len(new_urls) != 0:
			logger.warning('Some jobs failed. Updating job list with remaining urls.')
			for url in new_urls:
				scrape_job_list.write(f"{url}\n")
		else:
			logger.info('No jobs remaining.')

	with open(plot_list_directory, 'w') as plot_job_list:

		if len(completed_submission_ids) != 0:
			for sub_id in completed_submission_ids:
				plot_job_list.write(f"{sub_id}\n")
			logger.info('Successfully updated plot job list with submission ids.')
		else:
			logger.warning('Failure: Zero submissions were scraped successfully.')


# Login to Praw
reddit = RedditScraper()

'''
Read Job List
'''

# Set job list files
scrape_list_directory = 'job/scrape_job_list.txt'
plot_list_directory = 'job/plot_job_list.txt'

# Executes items in job list
new_urls, completed_submission_ids = execute_job_list()

# Removes scraped urls from job list and updates plot job list with new submissions
update_job_lists(new_urls, completed_submission_ids)

logger.info('Killing data_collector.py.')
