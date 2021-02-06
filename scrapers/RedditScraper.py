import os
from configparser import RawConfigParser
import praw


class RedditScraper:

    def __init__(self):

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

        try:
            # Login with password flow
            reddit = praw.Reddit(
                client_id=self.config['login']['client_id'],
                client_secret=self.config['login']['client_secret'],
                password=self.config['login']['password'],
                user_agent=self.config['login']['user_agent'],
                username=self.config['login']['username']
            )

            # Print username if login successful
            print(reddit.user.me())

        except KeyError as e:
            _error_message = 'Key error encountered while attempting to login. Ensure that your login file is \
            configured correctly and the program is running from root.'
            print(f'{e}\n{_error_message}')

        except Exception as e:
            _error_message = 'Unexpected error occurred.'
            print(f'{e}\n{_error_message}')

    def scrape_post(self):
        pass



if __name__ == '__main__':

    r = RedditScraper()
