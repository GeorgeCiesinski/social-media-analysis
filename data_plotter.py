from data_transformation.DataTransform import DataTransform
from entities.util.database_manager import DatabaseManager
from logs.Logger import base_logger

logger = base_logger.getChild(__name__)


def plot_all_graphs(database_manager, data_transform, submission_id):
	"""
	Receives a submission id and calls DataTransform functions to plot the data into graphs.

	:param DatabaseManager database_manager: Instance of DatabaseManager class used to interface with database
	:param DataTransform data_transform: Instance of DataTransform class used to plot graphs
	:param str submission_id: Submission.id for the submission
	"""

	# Create submission dict
	submission_dict = {
		'id': submission_id
	}

	# Populate submission_dict with information from database
	database_manager.extract_submission(submission_dict)

	# Extract comments_dict with comments and sentiment for submission
	comments_dict = database_manager.extract_comments_sentiment(submission_dict)

	# Create Dataframes
	comment_df, sentiment_stats, timeline_df = data_transform.create_df(submission_id, comments_dict)

	# Plot all graphs
	data_transform.reply_timeline(submission_id, timeline_df)
	data_transform.sentiment_timeline(submission_id, comment_df)
	data_transform.sentiment_pie(submission_id, comment_df)
	data_transform.total_comments_and_replies(submission_id, sentiment_stats)
	data_transform.total_comments_and_upvotes(submission_id, sentiment_stats)


def execute_job_list():

	# Instantiating empty lists for failed jobs
	new_sub_ids = []

	logger.info(f'Reading job/{plot_list_directory}.')

	# Read file and extract submission ids
	with open(plot_list_directory, "r") as plot_job_list:
		submission_ids = plot_job_list.read().splitlines()

	logger.info(f'Found {len(submission_ids)} jobs.')

	# For each Submission.id in submission_ids
	for submission in submission_ids:

		logger.info(f'Plotting submission: {submission}')

		try:
			# Plot all graphs
			plot_all_graphs(dm, dt, submission)
			logger.info('Removing submission from job list.')
		except Exception as e:
			logger.error('Unexpected error occurred. Aborted plotting submission.')
			logger.error(e)
			new_sub_ids.append(submission)

	return new_sub_ids


def update_job_list():

	with open(plot_list_directory, 'w') as plot_job_list:

		if len(new_sub_ids) != 0:
			for sub_id in new_sub_ids:
				plot_job_list.write(f"{sub_id}\n")
			logger.warning('Some submissions were not plotted successfully. Updated job list.')
		else:
			logger.info('Successfully plotted all submissions. Clearing job list.')


'''
INSTANTIATE CLASSES AND VARIABLES
'''

# Database Manager used to interface with database
dm = DatabaseManager()

# Data Transform used to plot graphs
dt = DataTransform()

# Set job list files
plot_list_directory = 'job/plot_job_list.txt'

'''
Read Job List
'''

# Executes items in job list
new_sub_ids = execute_job_list()

update_job_list()

logger.info('Killing data_plotter.py.')
