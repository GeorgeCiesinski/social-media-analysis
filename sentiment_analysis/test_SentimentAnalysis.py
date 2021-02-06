# import dependencies
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# run test script
t = 0
v = 0

def sentiment_analysis(sample):

    # TextBlobsentiment analysis
    analysis = TextBlob(sample)

    # print results
    print("\n=====TEXTBLOB======")
    if analysis.polarity > 0:
        print("{:.1f}".format(analysis.polarity), " Positive")
    elif analysis.polarity == 0:
        print("{:.1f}".format(analysis.polarity), " Neutral")
    else:
        print("{:.1f}".format(analysis.polarity), " Negative")

        # Vader sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sample)
    sentiment_dict = analyzer.polarity_scores(sample)
    print("\n======VADER========")
    print("{:.1f}".format(sentiment_dict['neg'] * -1), " Negative")
    print("{:.1f}".format(sentiment_dict['neu']), " Neutral")
    print("{:.1f}".format(sentiment_dict['pos']), " Positive")
    print("{:.1f}".format(sentiment_dict['compound']), " Compound")