
#import dependencies
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


#run test script
sample = ""
t = 0
v = 0

while sample != "stop":

    print("-------------------\n") 
    sample = input("Enter sample sentence: \n")

    if sample == "stop":
           break

    if sample == "check":
           print("\n--------------SCORE------------\n") 
           print(f"TexBlob : {t}\nVader : {v}\n")  
           continue   
       
    #TextBlobsentiment analysis
    analysis = TextBlob(sample)

    #print results 
    print("\n=====TEXTBLOB======")  
    if analysis.polarity > 0:
           print("{:.1f}".format(analysis.polarity), " Positive") 
    elif analysis.polarity == 0:
           print("{:.1f}".format(analysis.polarity), " Neutral") 
    else:
        print("{:.1f}".format(analysis.polarity), " Negative") 

    #Vader sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sample)
    sentiment_dict = analyzer.polarity_scores(sample) 
    print("\n======VADER========")  
    print("{:.1f}".format(sentiment_dict['neg']*-1), " Negative") 
    print("{:.1f}".format(sentiment_dict['neu']), " Neutral") 
    print("{:.1f}".format(sentiment_dict['pos']), " Positive") 
    print("{:.1f}".format(sentiment_dict['compound']), " Compound")

    #score
    score = input("\nWhich method is more accurate? [t/v] ")
    if score == "t":
       t +=1
    elif score == "v":
       v +=1
    elif score == "tie":
       t+=1
       v+=1       
print("\n---------FINAL SCORE------------\n") 
print(f"TexBlob : {t}\nVader : {v}\n")             