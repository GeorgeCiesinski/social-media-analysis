from data_transformation.DataTransform import DataTransform
from logs.Logger import base_logger

logger = base_logger.getChild(__name__)



'''
INSTANTIATE (TEMP)
'''

# Instantiate DataTransform
df = DataTransform()

'''
GRAPHS
'''

df.overall_sentiment_replies(comments_dict)
df.overall_sentiment_upvotes(comments_dict)
df.sentiment_pie(comments_dict)
df.sentiment_timeline(comments_dict)




job_list_directory = 'plot_job_list.txt'

logger.info(f'Reading job/{job_list_directory}.')

# Read file and plot each url
with open(job_list_directory, "r") as plot_job_list:
	urls = plot_job_list.readlines()

logger.info(f'Found {len(urls)} jobs.')

for url in urls:

	logger.info(f'Scraping url: {url}')
	scrape_submission(url)