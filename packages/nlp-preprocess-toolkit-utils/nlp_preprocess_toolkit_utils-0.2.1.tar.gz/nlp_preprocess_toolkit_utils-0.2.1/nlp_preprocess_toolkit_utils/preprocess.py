# preprocess.py

import pandas as pd
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Preprocessing Function
def preprocess_text(text):
    """Preprocess the given text with multiple NLP steps."""
    text = text.lower()

    # Remove actual URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove the word "url" if it exists in the input text
    text = re.sub(r'\burl\b', '', text)

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    tokens = [word for word in tokens if word.isalnum()]

    return ' '.join(tokens)


def read_file(file_path):
    """Reads different file types and returns their content as a string."""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        return ' '.join(df.astype(str).values.flatten())
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        return ' '.join(df.astype(str).values.flatten())
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        raise ValueError("Unsupported file type. Please use .csv, .xlsx, or .txt.")

def read_from_url(url):
    """Fetches text content from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError("Failed to retrieve content from URL.")

def generate_word_cloud(text):
    """Generates and displays a word cloud from the given text."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
