from sqlalchemy.orm import joinedload
from entities.base import Session
from entities.submission import Submission
from entities.comment import Comment
from entities.sentiment import Sentiment

# exceptions
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# logging
from logs.Logger import base_logger


logger = base_logger.getChild(__name__)


class DatabaseManager:

	# Handle session setup and destruction
	def __init__(self):
		self.session = Session()

	def __del__(self):
		self.session.close()

	'''
	INFORMATION
	'''

	def check_submission_exists(self, submission_dict):
		"""
		Checks if a submission id already exists in database, and returns True or False.

		:param dict submission_dict: Dict containing submission information
		:return bool submission_exists: Value representing whether submission exists in database
		"""

		submission_id = submission_dict.get('id')

		submission = None

		logger.info(f'Checking if submission {submission_id} exists in the database.')

		# Check if the submission exists using id
		try:
			submission = self.session.query(Submission) \
				.filter(Submission.id == submission_id) \
				.one()
			logger.info(f'Found submission {submission_id} in the database.')
		except(NoResultFound, MultipleResultsFound) as e:
			logger.warning(f'Could not find submission {submission_id} in the database.')
			logger.warning(e)

		return submission

	def get_submission_ids(self):
		"""
		Queries the database for submissions, and creates a list of submission_id's.

		:return list submission_id_list: List of submission id's in the database
		"""

		logger.info('Getting list of submissions from database.')

		submission_list = self.session.query(Submission) \
			.all()

		# Creates list of Submission.id's for each submission item in submission_list
		submission_id_list = [submission_item.id for submission_item in submission_list]

		return submission_id_list

	'''
	DATABASE INSERTION
	'''

	def insert_submission(self, submission_dict):
		"""
		Creates a submission object, inserts into the database, and returns the object with newly generated id.

		:param dict submission_dict: Dict containing submission information
		:return Submission submission: An instance of the Submission object
		"""

		submission_id = submission_dict.get('id')
		logger.info(f'Inserting {submission_id} into database.')

		# Insert Submission Data

		new_submission = Submission(
			id=submission_dict.get('id'),
			title=submission_dict.get('title'),
			selftext=submission_dict.get('selftext'),
			score=submission_dict.get('score'),
			created_utc=submission_dict.get('created_utc'),
		)

		self.session.add(new_submission)

		try:
			self.session.commit()
			logger.info('Successfully inserted into database.')
		except IntegrityError as e:
			# In case of integrity error, log error and return None
			logger.error(f'Unable to insert Submission {submission_id} into database due to Integrity Error.')
			logger.error(e)
			return None

		return new_submission

	def insert_comments(self, comments_dict, submission):
		"""
		Iterates through the list of comments and creates comment objects. Inserts the comment objects into the
		database.

		:param dict comments_dict: Dict containing a list of comment dicts
		:param Submission submission: An instance of the Submission object
		"""

		logger.info(f'Inserting comments from submission {submission.id} into database.')

		# Extract comment_data from comments_dict
		comment_data = comments_dict.get('data')

		# Iterate through comment_data and add sentiment_result list
		for comment in comment_data:

			new_comment = Comment(
				id=comment.get('id'),
				submission_id=submission.id,
				author=comment.get('author'),
				body=comment.get('body'),
				score=comment.get('score'),
				saved=comment.get('saved'),
				number_of_replies=comment.get('number_of_replies'),
				created_utc=comment.get('created_utc'),
			)

			self.session.add(new_comment)

		self.session.commit()

		logger.info('Successfully inserted comments into database.')

	def insert_sentiment(self, comments_dict):
		"""
		Iterates through the list of comments, extracts sentiment data,  and creates sentiment objects. Inserts the
		sentiment objects into the database.

		:param dict comments_dict: Dict containing a list of comment dicts
		"""

		logger.info('Inserting sentiment into database.')

		# Extract comment_data from comments_dict
		comment_data = comments_dict.get('data')

		# Iterate through comment_data and add sentiment_result list
		for comment in comment_data:

			# Extract sentiment dict from comment dict
			_sentiment_dict = comment.get('sentiment')

			new_sentiment = Sentiment(
				comment_id=comment.get('id'),
				polarity=_sentiment_dict.get('polarity'),
				sentiment=_sentiment_dict.get('sentiment')
			)

			self.session.add(new_sentiment)

		self.session.commit()

		logger.info('Successfully inserted sentiment into database.')

	'''
	DATABASE EXTRACTION
	'''

	def extract_submission(self, submission_dict):
		"""
		Receives partial submission_dict, which must at least include the id. Finds the submission in the database
		and replaces the data in the dict with data from the database. Does not return anything as submission_dict is
		mutable.

		:param dict submission_dict: Partial or complete submission_dict containing at least the id.
		"""

		# Get submission id
		submission_id = submission_dict.get('id')

		logger.info(f'Extracting submission {submission_id} from the database.')

		try:
			# Extract result from database
			result = self.session.query(Submission) \
				.filter(Submission.id == submission_id) \
				.one()
			submission_dict = result.asdict()

			logger.info(f'Successfully extracted submission {submission_id} from the database.')

		except (NoResultFound, MultipleResultsFound) as e:
			_error_message = f'Unable to find submission {submission_id} in database.'
			logger.error(_error_message)
			logger.error(e)
			submission_dict = {
				'error': _error_message
			}

	def extract_comments(self, submission_dict):
		"""
		Receives partial submission_dict, which must at least include the id. Creates a comments_dict and populates it
		with comments with the same id. Returns comments_dict. DOES NOT INCLUDE SENTIMENT DATA.

		:param dict submission_dict: Partial or complete submission_dict containing at least the id.
		:return dict comments_dict: Dict containing data, which is a list of individual comment dicts.
		"""

		# Get submission id
		submission_id = submission_dict.get('id')

		logger.info(f'Extracting comments from submission {submission_id} from the database.')

		# Extract result from database
		result = self.session.query(Comment) \
			.filter(Comment.submission_id == submission_id) \
			.all()

		# Store comments as dicts in a list stored in the 'data' key.
		comments_dict = {
			'data': [
				item.asdict()
				for item in result
			]
		}

		logger.info(f'Successfully extracted comments from submission {submission_id} from the database.')

		return comments_dict

	def extract_sentiment(self, comment_id):
		"""
		TBA, function is incomplete.

		:param str comment_id: A string id representing the comment the sentiment is for.
		:return list sentiment: A list containing the polarity and sentiment.
		"""

		# Todo: complete this later

		pass

	def extract_comments_sentiment(self, submission_dict):
		"""
		Receives partial submission_dict, which must at least include the id. Creates a comments_dict and populates it
		with comments with the same id as well as their sentiment data. Returns comments_dict.

		:param dict submission_dict: Partial or complete submission_dict containing at least the id.
		:return dict comments_dict: Dict containing comment and sentiment data.
		"""

		# Get submission id
		submission_id = submission_dict.get('id')

		logger.info(f'Extracting comments and sentiment for submission {submission_id} from the database.')

		result = self.session.query(Comment) \
			.filter(Comment.submission_id == submission_id) \
			.options(
				joinedload(Comment.sentiment)
			).all()

		# Store comments as dicts in a list stored in the 'data' key.
		comments_dict = {
			'data': [
				# Use asdict to return a dict of columns/keys and values
				item.asdict(
					follow={
						# append sentiment data from joinedload query to Comment dict
						'sentiment': {
							# Only include polarity and sentiment columns
							'only': [
								'polarity',
								'sentiment'
							]
						}
					}
				)
				for item in result
			]
		}

		logger.info(f'Successfully extracted comments and sentiment for submission {submission_id} from the database.')

		return comments_dict

	'''
	DATABASE DELETION
	'''

	def delete_submission(self, submission_dict):
		"""
		Deletes the submission from the submission table, as well as child entries in the comment and sentiment tables.
		Adds a new key to submission_dict indicating whether the delete was successful or not.

		:param submission_dict:
		"""

		submission_id = submission_dict.get('id')

		logger.info(f'Deleting submission, comments, and sentiment for submission {submission_id} from the database.')

		submission = None

		# Check if the submission exists using id
		try:
			submission = self.session.query(Submission) \
				.filter(Submission.id == submission_id) \
				.one()
		except(NoResultFound, MultipleResultsFound) as e:
			logger.warning(f'Could not find submission_id {submission_id} in the database.')
			logger.warning(e)

		# Delete the Submission
		try:
			self.session.delete(submission)
			self.session.commit()

			submission_dict['submission_deleted'] = True

			logger.info(f'Successfully deleted data for submission {submission_id} from the database.')

		except Exception as e:
			# If an unexpected exception occurred, handle it
			logger.error('Unexpected exception occurred:')
			logger.error(e)

			submission_dict['submission_deleted'] = False

			logger.info(f'Failed to delete data for submission {submission_id} from the database.')
