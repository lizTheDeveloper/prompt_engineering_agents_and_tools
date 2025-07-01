import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

def download_dependencies():
    """
    Downloads necessary NLTK resources.
    """
    nltk.download('vader_lexicon')
    nltk.download('punkt')

def analyze_sentiment(text):
    """
    Analyzes the sentiment of each sentence in the provided text.

    Parameters:
    text (str): The corpus of text to be analyzed.

    Returns:
    list of float: Sentiment scores for each sentence.
    """
    # Initialize the SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Analyze sentiment for each sentence
    sentiment_scores = [sid.polarity_scores(sentence)['compound'] for sentence in sentences]
    return sentiment_scores

def plot_sentiment(sentiment_scores):
    """
    Plots the sentiment scores as a line graph.

    Parameters:
    sentiment_scores (list of float): Sentiment scores for each sentence.
    """
    # Generate x values as ordinal numbers for each sentence
    x = list(range(1, len(sentiment_scores) + 1))
    
    # Create a plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, sentiment_scores, marker='o')
    plt.title('Sentence-by-Sentence Sentiment Analysis')
    plt.xlabel('Sentence Number')
    plt.ylabel('Sentiment Score')
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to perform the sentiment analysis and plot the results.
    """
    # Sample text for demonstration
    text = "This is a great day. I am so happy. But then it started to rain. I don't like rain. However, the rainbow was beautiful."

    # Download necessary NLTK resources
    download_dependencies()

    # Perform sentiment analysis
    sentiment_scores = analyze_sentiment(text)

    # Plot the sentiment scores
    plot_sentiment(sentiment_scores)

if __name__ == '__main__':
    main()
