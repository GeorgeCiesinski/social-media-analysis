"""
Author: George Ciesinski
Date: Feb 06 2021
Latest update: Mar 13 2021
"""

import os
from datetime import datetime
from configparser import RawConfigParser
import praw
from prawcore.exceptions import NotFound

# logging
from logs.Logger import base_logger


logger = base_logger.getChild(__name__)


class RedditScraper:

    def __init__(self):
        """
        Logs into reddit and creates a self.reddit object to be used in the rest of Reddit Scraper
        """

        logger.info('Reading PRAW login config.')

        # Set Config Directory
        _config_dir = 'config'
        _config_filename = os.path.join(_config_dir, 'login.ini')
        print(f'Config directory: {_config_filename}')

        # Read login config file
        self.config = RawConfigParser()
        self.config.read(_config_filename)

        '''
        LOGIN
        '''

        logger.info('Attempting PRAW login.')

        try:
            # Login with password flow
            self.reddit = praw.Reddit(
                client_id=self.config['login']['client_id'],
                client_secret=self.config['login']['client_secret'],
                password=self.config['login']['password'],
                user_agent=self.config['login']['user_agent'],
                username=self.config['login']['username']
            )

            user_name = self.reddit.user.me()
            logger.info(f'Successfully logged in as {user_name}.')

        except KeyError as e:
            _error_message = 'Key error encountered while attempting to login. Ensure that your login file is \
            configured correctly and the program is running from root.'
            logger.error(f'{e}\n{_error_message}')

        except Exception as e:
            _error_message = 'Unexpected error occurred.'
            logger.error(f'{e}\n{_error_message}')

    @staticmethod
    def unix_to_datetime(unix_time):

        time_stamp = int(unix_time)

        date_time = datetime.utcfromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

        return date_time

    def extract_post_data(self, submission_id=None, submission_url=None):
        """
        Creates a submission object and populates it with submission data from reddit. Either a submission id or
        a submission_url is required.

        :param str submission_url: Praw Submission.url
        :param str submission_id: Praw Submission.id
        :return dict submission_dict: Dict containing submission object and raw information
        """

        '''
        Get submission object
        '''

        error_message = None
        submission = None
        submission_dict = {}

        if submission_id and not submission_url:

            logger.info(f'Extracting post data for submission id: {submission_id}')
            submission = self.reddit.submission(id=submission_id)

        elif submission_url and not submission_id:

            logger.info(f'Extracting post data for submission url: {submission_url}')
            submission = self.reddit.submission(url=submission_url)

        elif submission_id and submission_url:

            error_message = 'Please provide either a submission id or a submission url, not both.'

        '''
        Populate submission_dict
        '''

        if submission:

            try:
                # Create submission dict using values from submission object
                submission_dict = {
                    'submission_object': submission,
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'subreddit': submission.subreddit,
                    'author': submission.author,
                    'score': submission.score,
                    'upvote_ratio': submission.upvote_ratio,
                    'locked': submission.locked,
                    'id': submission.id,
                    'url': submission.url,
                    'created_utc': self.unix_to_datetime(submission.created_utc),
                    'error': None
                }

                logger.info(f'Completed extracting post data.')

            except NotFound:
                if submission_id:
                    feedback = f'id: {submission_id}.'
                elif submission_url:
                    feedback = f'url: {submission_url}.'
                error_message = f'Received 404 HTTP response while trying to get submission using {feedback}'
                logger.error(error_message)

        if error_message:
            logger.error(error_message)
            submission_dict = {
                'error': error_message
            }

        return submission_dict

    def extract_post_comments_data(self, submission):
        """
        Receives a submission object, and extracts all of the root level comments. Creates a dict for each comment
        and appends it to a list, which is then inserted into comments_dict and returned.

        :param Submission submission: PRAW Submission object
        :return dict comments_dict: Dict containing data, which is a list of dicts
        """

        comments_list = []
        comments_dict = {}

        logger.info(f'Extracting comment data for submission id: {submission.id}.')

        try:
            # Replace all
            submission.comments.replace_more(limit=None)

            for top_level_comment in submission.comments:

                # Replace all replies
                top_level_comment.replies.replace_more(limit=None)

                # Todo: Fix using debugger | __len__
                number_of_replies = len(top_level_comment.replies)

                comment = {
                    'id': top_level_comment.id,
                    'author': top_level_comment.author.name if top_level_comment.author is not None else '[deleted]',
                    'body': top_level_comment.body,
                    'score': top_level_comment.score,
                    'saved': top_level_comment.saved,
                    'number_of_replies': number_of_replies,
                    'created_utc': self.unix_to_datetime(top_level_comment.created_utc)
                }

                comments_list.append(comment)

            comments_dict = {
                "data": comments_list
            }

            logger.info(f'Completed extracting comment data.')

        except TypeError as e:

            logger.error('Failed to extract comments data due to TypeError.')
            logger.error(e)

        except AttributeError as e:

            logger.error('Failed to extract comments data due to AttributeError.')
            logger.error(e)

        except Exception as e:
            logger.error(f'Encountered unexpected error: \n {e}')
            comments_dict = {
                "error": "Unable to populate comments_dict. Check log files."
            }

        return comments_dict
