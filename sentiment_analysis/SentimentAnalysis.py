from textblob import TextBlob


def list_parser(comments_dict):

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

    # TextBlobsentiment analysis
    analysis = TextBlob(body)

    if analysis.polarity > 0:
        result = [analysis.polarity, " Positive"]
    elif analysis.polarity == 0:
        result = [analysis.polarity, " Neutral"]
    else:
        result = [analysis.polarity, " Negative"]

    return result
