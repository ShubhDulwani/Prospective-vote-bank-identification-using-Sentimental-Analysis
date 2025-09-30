# Election Sentiment Analyzer

A web application for analyzing election-related sentiment from CSV data using natural language processing. This tool helps predict election outcomes by analyzing public opinion through text sentiment analysis.

## Features

- **CSV File Upload**: Upload CSV files containing election-related text data
- **Sentiment Analysis**: Automated sentiment scoring using natural language processing
- **Visual Analytics**: Interactive charts and visualizations including:
  - Sentiment distribution pie charts
  - Sentiment score histograms
  - Real-time animated statistics
- **Election Predictions**: AI-powered predictions based on sentiment analysis
- **Downloadable Results**: Export processed data with sentiment scores
- **Responsive Design**: Mobile-friendly interface with modern UI

## How It Works

1. **Upload CSV**: Upload a CSV file containing election-related text data
2. **Processing**: The system cleans text, removes stopwords, and analyzes sentiment
3. **Results**: View detailed sentiment analysis with visualizations and predictions

## Getting Started

### Prerequisites

- Python 3.7+
- Flask web framework
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/election-sentiment-analyzer.git
cd election-sentiment-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## File Structure

```
election-sentiment-analyzer/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html         # Main upload page
│   └── results.html       # Results display page
├── static/
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── script.js      # Client-side functionality
├── uploads/               # Temporary file storage
├── processed/             # Processed results storage
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## CSV File Format

Your CSV file should contain at least one column with text content to analyze. Common column names include:
- `text`
- `content`
- `message`
- `comment`
- `tweet`

Example CSV structure:
```csv
id,text,date
1,"Great policies for our future!",2024-01-15
2,"Not sure about this candidate",2024-01-16
3,"Terrible decision making",2024-01-17
```

## Features in Detail

### Sentiment Analysis
- **Positive Sentiment**: Scores from 0.1 to 1.0
- **Neutral Sentiment**: Scores from -0.1 to 0.1
- **Negative Sentiment**: Scores from -1.0 to -0.1

### Visualizations
- **Pie Chart**: Shows distribution of positive, neutral, and negative sentiments
- **Histogram**: Displays the spread of sentiment scores across the dataset
- **Animated Statistics**: Real-time counting animations for engagement

### Election Predictions
The system uses sentiment analysis to provide insights into potential election outcomes based on:
- Overall sentiment distribution
- Average sentiment score
- Historical correlation patterns

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main upload page |
| `/upload` | POST | Handle file upload and processing |
| `/results/<filename>` | GET | Display analysis results |
| `/download/<filename>` | GET | Download processed CSV |

## Security Features

- File type validation (CSV only)
- Secure file handling with unique identifiers
- Local processing (no data sharing with third parties)
- Input sanitization and validation

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Dependencies

Key Python packages:
- Flask - Web framework
- pandas - Data manipulation
- nltk - Natural language processing
- matplotlib/seaborn - Data visualization
- scikit-learn - Machine learning utilities

## Troubleshooting

### Common Issues

**File Upload Errors**
- Ensure your CSV file is properly formatted
- Check that the file size is under the upload limit
- Verify the file contains text data to analyze

**Processing Errors**
- Make sure your CSV has at least one column with text content
- Check for encoding issues (UTF-8 recommended)
- Ensure the CSV is not corrupted

**Visualization Issues**
- Clear browser cache and cookies
- Ensure JavaScript is enabled
- Try using a different browser

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Flask and modern web technologies
- Utilizes NLTK for natural language processing
- Font Awesome icons for UI elements
- Chart.js for data visualizations

## Contact

For questions or support, please open an issue on GitHub or contact the development team.

---

**Note**: This tool provides sentiment analysis for educational and research purposes. Election predictions should be considered alongside other factors and professional analysis for any serious political decision-making.