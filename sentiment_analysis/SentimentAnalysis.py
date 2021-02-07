# import dependencies
from textblob import TextBlob

def list_parser(redditData):

    for comment in redditData:
        body = comment.get('body')
        sentiment_result = sentiment_analysis(body)
        comment['sentiment'] = sentiment_result

def sentiment_analysis(body):

    # TextBlobsentiment analysis
    analysis = TextBlob(body)

    if analysis.polarity > 0:
        result = [analysis.polarity, " Positive"]
    elif analysis.polarity == 0:
        result = [analysis.polarity, " Neutral"]
    else:
        result = [analysis.polarity, " Negative"]

    return result