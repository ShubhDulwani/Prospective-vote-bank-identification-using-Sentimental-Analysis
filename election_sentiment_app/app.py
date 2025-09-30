import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = "election_sentiment_analyzer"
app.config['UPLOAD_FOLDER'] = 'data'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def clean_text(text):
    if isinstance(text, str):
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        # Convert to lowercase
        text = text.lower()
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(filtered_tokens)
    return ""

def analyze_sentiment(text):
    if not isinstance(text, str) or not text.strip():
        return 0  # Neutral sentiment for empty or non-string input
    
    analysis = TextBlob(text)
    # Return polarity score (-1 to 1)
    return analysis.sentiment.polarity

def process_csv(file_path):
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Check if CSV has required columns
        text_column = None
        for col in df.columns:
            if col.lower() in ['text', 'comment', 'message', 'tweet', 'statement', 'content']:
                text_column = col
                break
        
        if text_column is None and len(df.columns) > 0:
            # If no matching column found, use the first column that appears to have text
            for col in df.columns:
                if df[col].dtype == 'object':
                    text_column = col
                    break
        
        if text_column is None:
            return None, "Could not identify a text column in the CSV file."
        
        # Create a copy to avoid modifying the original
        processed_df = df.copy()
        
        # Clean text and analyze sentiment
        processed_df['cleaned_text'] = processed_df[text_column].apply(clean_text)
        processed_df['sentiment_score'] = processed_df['cleaned_text'].apply(analyze_sentiment)
        
        # Categorize sentiment
        processed_df['sentiment_category'] = pd.cut(
            processed_df['sentiment_score'],
            bins=[-1.1, -0.3, 0.3, 1.1],
            labels=['Negative', 'Neutral', 'Positive']
        )
        
        return processed_df, None
    except Exception as e:
        return None, f"Error processing CSV: {str(e)}"

def generate_summary(df):
    # Count sentiments
    sentiment_counts = df['sentiment_category'].value_counts()
    
    # Calculate percentages
    total = sentiment_counts.sum()
    percentages = {
        'Positive': round((sentiment_counts.get('Positive', 0) / total) * 100, 2),
        'Neutral': round((sentiment_counts.get('Neutral', 0) / total) * 100, 2),
        'Negative': round((sentiment_counts.get('Negative', 0) / total) * 100, 2)
    }
    
    # Calculate average sentiment
    avg_sentiment = df['sentiment_score'].mean()
    
    # Prediction
    if avg_sentiment > 0.1:
        prediction = "Positive public opinion likely indicates favorable election outcomes."
    elif avg_sentiment < -0.1:
        prediction = "Negative public opinion suggests challenging election prospects."
    else:
        prediction = "Mixed or neutral sentiment indicates a closely contested election."
    
    return {
        'sentiment_counts': sentiment_counts.to_dict(),
        'percentages': percentages,
        'avg_sentiment': round(avg_sentiment, 4),
        'prediction': prediction
    }

def generate_charts(df):
    charts = {}
    
    # Sentiment distribution pie chart
    plt.figure(figsize=(8, 6))
    sentiment_counts = df['sentiment_category'].value_counts()
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['red', 'gray', 'green'])
    plt.title('Sentiment Distribution')
    
    # Save to base64 string for embedding in HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    pie_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    charts['pie_chart'] = pie_chart
    plt.close()
    
    # Sentiment histogram
    plt.figure(figsize=(8, 6)) 
    plt.hist(df['sentiment_score'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Sentiment Score Distribution')
    plt.xlabel('Sentiment Score (-1 to 1)')
    plt.ylabel('Frequency')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    histogram = base64.b64encode(buffer.getvalue()).decode('utf-8')
    charts['histogram'] = histogram
    plt.close()
    
    return charts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Process the file
        processed_df, error = process_csv(file_path)
        
        if error:
            flash(error)
            return redirect(url_for('index'))
        
        # Generate summary and charts
        summary = generate_summary(processed_df)
        charts = generate_charts(processed_df)
        
        # Save processed data
        processed_file = f"processed_{unique_filename}"
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_file)
        processed_df.to_csv(processed_path, index=False)
        
        return render_template(
            'results.html',
            summary=summary,
            charts=charts,
            filename=filename,
            processed_file=processed_file
        )
    else:
        flash('File type not allowed. Please upload a CSV file.')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    # Add security check to prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        flash('Invalid file access')
        return redirect(url_for('index'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)