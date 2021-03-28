from data_transformation.DataTransform import DataTransform
from logs.Logger import base_logger

logger = base_logger.getChild(__name__)

# Instantiate DataTransform
df = DataTransform()

'''
TEMPORARY GRAPHS
'''
df.overall_sentiment_replies(comments_dict)
df.overall_sentiment_upvotes(comments_dict)
df.sentiment_pie(comments_dict)
df.sentiment_timeline(comments_dict)