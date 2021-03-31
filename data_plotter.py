from data_transformation.DataTransform import DataTransform
from entities.util.database_manager import DatabaseManager
from logs.Logger import base_logger

logger = base_logger.getChild(__name__)


def plot_all_graphs(data_transform, submission_id):
	"""
	Receives a submission id and calls DataTransform functions to plot the data into graphs.

	:param DataTransform data_transform: Instance of DataTransform class used to plot graphs
	:param str submission_id: Submission.id for the submission
	"""

	# Create submission dict
	submission_dict = {
		'id': submission_id
	}

	# Populate submission_dict with information from database
	DatabaseManager.extract_submission(submission_dict)

	# Extract comments_dict with comments and sentiment for submission
	comments_dict = DatabaseManager.extract_comments_sentiment(submission_dict)

	# Plot Graphs
	data_transform.overall_sentiment_replies(comments_dict)
	data_transform.overall_sentiment_upvotes(comments_dict)
	data_transform.sentiment_pie(comments_dict)
	data_transform.sentiment_timeline(comments_dict)


'''
INSTANTIATE CLASSES
'''

dt = DataTransform()

'''
Read Job List
'''

job_list_directory = 'plot_job_list.txt'

logger.info(f'Reading job/{job_list_directory}.')

# Read file and extract submission ids
with open(job_list_directory, "r") as plot_job_list:
	submission_ids = plot_job_list.readlines()

logger.info(f'Found {len(submission_ids)} jobs.')

# For each Submission.id in submission_ids
for submission in submission_ids:
	# Plot all graphs
	logger.info(f'Plotting submission: {submission}')
	plot_all_graphs(dt, submission)
