"""
Author: Saif Gorges
Date: March 15 2021
"""

from textblob import TextBlob


def list_parser(comments_dict):
    """
    Parses through comments dictionary and appends sentiment analysis.

    :param dict comments_dict: Dict containing comments information.
    :return dict comments_dict: Returned dict containing sentiment analysis.
    """
    # Extract comment_data from comments_dict
    comment_data = comments_dict.get('data')

    # Iterate through comment_data and add sentiment_result list
    for comment in comment_data:
        body = comment.get('body')
        sentiment_result = sentiment_analysis(body)
        comment['sentiment'] = sentiment_result

    # Updates comments_dict with modified data
    comments_dict['data'] = comment_data


def sentiment_analysis(body):
    """
    Performs sentiment analysis on text and returns list with value and description of sentiment.

    :param string body: String containing comment data.
    :return list result: Returned list containing value and description of sentiment.
    """
    # TextBlobsentiment analysis
    analysis = TextBlob(body)

    if analysis.polarity > 0:
        result = [analysis.polarity, " Positive"]
    elif analysis.polarity == 0:
        result = [analysis.polarity, " Neutral"]
    else:
        result = [analysis.polarity, " Negative"]

    return result
