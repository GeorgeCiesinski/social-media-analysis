"""
Author: Saif Gorges
Date: March 11 2021
"""

# Import dependencies
import pandas as pd
import matplotlib.pyplot as plt


class DataTransform:

    @staticmethod
    def create_df(comments_dict):

        # Create empty lists
        author = []
        body = []
        created_utc = []
        id = []
        number_of_replies = []
        saved = []
        score = []
        sentiment_polarity = []
        sentiment_description = []

        # Parse through json file and append lists
        for x in range(len(comments_dict['data'])):
            author.append(comments_dict['data'][x]['author'])
            body.append(comments_dict['data'][x]["body"])
            created_utc.append(comments_dict['data'][x]["created_utc"])
            id.append(comments_dict['data'][x]['id'])
            number_of_replies.append(comments_dict['data'][x]["number_of_replies"])
            saved.append(comments_dict['data'][x]['saved'])
            score.append(comments_dict['data'][x]["score"])
            sentiment_polarity.append(comments_dict['data'][x]["sentiment"]["polarity"])
            sentiment_description.append(comments_dict['data'][x]["sentiment"]["sentiment"])

        # Create and clean dataframe
        comment_df = pd.DataFrame(
            zip(author, body, created_utc, id, number_of_replies, saved, score, sentiment_polarity,
                sentiment_description))

        # rename columns
        comment_df = comment_df.rename(
            columns={0: "Author", 1: "Comment", 2: "Date", 3: "ID", 4: "Number of Replies", 5: "Saved", 6: "Upvotes",
                     7: "Sentiment Polarity", 8: "Sentiment Description"})
        comment_df['Sentiment Polarity'] = pd.DataFrame(comment_df['Sentiment Polarity'].values.tolist())
        comment_df.head()

        # create bins column
        bins = [-1, -.75, -.5, -.25, 0, .25, .5, .75, 1]
        comment_df['Sentiment Range'] = pd.cut(comment_df['Sentiment Polarity'], bins)

        comment_df.head()

        # Transform dataframe to model stats for sentiment
        sentiment_stats = comment_df.groupby("Sentiment Range").agg(
            id_count=('ID', 'count'),
            score_sum=('Upvotes', 'sum'),
            replies_count=('Number of Replies', 'sum'),
        )
        sentiment_stats = sentiment_stats.reset_index()
        sentiment_stats['Sentiment Range'] = sentiment_stats['Sentiment Range'].astype(str)

        # Rename DataFrame
        sentiment_stats = sentiment_stats.rename(
            columns={"id_count": "Total Count", "score_sum": "Total Upvotes", "replies_count": "Total Replies"})

        return comment_df, sentiment_stats

    def overall_sentiment_upvotes(self, comments_dict):

        comment_df, sentiment_stats = self.create_df(comments_dict)
        # Creating axes object and defining plot for "Overall Sentiment & Upvotes
        ax = sentiment_stats.plot(kind='bar', x='Sentiment Range',
                                  y='Total Count', color='Blue',
                                  linewidth=3, rot=90)

        ax2 = sentiment_stats.plot(kind='line', x='Sentiment Range',
                                   y='Total Upvotes', secondary_y=True,
                                   color='Red', linewidth=3, rot=90,
                                   ax=ax)

        # Title of the plot
        plt.title("Overall Sentiment & Upvotes")

        # Labeling x and y-axis
        ax.set_xlabel('Sentiment Range', color='black')
        ax.set_ylabel('Sentiment Count', color="b")
        ax2.set_ylabel('Total Upvotes', color='r')

        # Defining display layout
        plt.tight_layout()

        # Show plot
        plt.savefig("data_transformation/Graphs/overall_sentiment_and_upvotes.png")
        plt.show()

    def overall_sentiment_replies(self, comments_dict):
        comment_df, sentiment_stats = self.create_df(comments_dict)
        # Creating axes object and defining plot
        ax = sentiment_stats.plot(kind='bar', x='Sentiment Range',
                                  y='Total Count', color='Blue',
                                  linewidth=3, rot=90)

        ax2 = sentiment_stats.plot(kind='line', x='Sentiment Range',
                                   y='Total Replies', secondary_y=True,
                                   color='Green', linewidth=3, rot=90,
                                   ax=ax)

        # Title of the plot
        plt.title("Overall Sentiment & Total Replies")

        # Labeling x and y-axis
        ax.set_xlabel('Sentiment Range', color='black')
        ax.set_ylabel('Sentiment Count', color="b")
        ax2.set_ylabel('Total Replies', color='g')

        # Defining display layout
        plt.tight_layout()

        # Show plot
        plt.savefig("data_transformation/Graphs/overall_sentiment_and_replies.png")
        plt.show()

    def sentiment_timeline(self, comments_dict):
        comment_df, sentiment_stats = self.create_df(comments_dict)
        # Create scatterplot for timeline vs sentiment

        ax1 = comment_df.plot.scatter(x='Date', y='Sentiment Polarity', c='Upvotes', colormap="viridis", rot=90)
        plt.savefig("data_transformation/Graphs/sentiment_timeline.png")

        # Create DataFrame for sentiment description
    def sentiment_pie(self, comments_dict):
        comment_df, sentiment_stats = self.create_df(comments_dict)
        sentiment_description_df = comment_df.groupby("Sentiment Description").agg(
            total_count=('ID', 'count')
        )

        # Create pie graph for sentiment distribution
        comment_df, sentiment_stats = self.create_df(comments_dict)
        sentiment_description_df = comment_df.groupby("Sentiment Description").agg(
            total_count=('ID', 'count')
        )

        sentiment_pie = sentiment_description_df.plot.pie(y='total_count', figsize=(5, 5), shadow=True,
                                                          autopct='%1.1f%%')
        plt.savefig("Graphs/sentiment_pie.png")
