# QuickShop: Tokopedia Product Analysis

QuickShop is a Streamlit-based web application designed for analyzing product reviews from Tokopedia, Indonesia's largest e-commerce platform. The app leverages advanced sentiment analysis techniques and integrates with the Groq API to provide intelligent chatbot functionality for product insights.

## Features

- **Product Review Scraping**: Automatically scrape customer reviews from Tokopedia product pages
- **Sentiment Analysis**: Analyze review sentiments using pre-trained Indonesian language models (IndoBERT)
- **Data Visualization**: Generate interactive charts and word clouds to visualize sentiment distribution
- **AI-Powered Chatbot**: Interact with a Groq-powered chatbot for product recommendations and insights
- **Data Export**: Save analyzed product data for further analysis

## Requirements

- Python 3.8+
- Chrome browser (for web scraping)
- Groq API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd capstone_new
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r Requirements.txt
   ```

4. Set up your Groq API key:
   - Create a `.env` file in the root directory
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here`

## Usage

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to the provided local URL (usually `http://localhost:8501`)

4. Use the app:
   - Enter a Tokopedia product URL
   - Click "Analyze Product" to scrape and analyze reviews
   - View sentiment analysis results, charts, and word clouds
   - Chat with the AI assistant for product insights

## Project Structure

```
capstone_new/
├── app.py                 # Main Streamlit application
├── Requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Directory for storing scraped data
├── helpers/              # Helper modules
│   ├── __init__.py
│   ├── analyzer.py       # Sentiment analysis functions
│   ├── config.py         # Configuration settings
│   ├── groq_client.py    # Groq API integration
│   ├── scraper.py        # Web scraping functions
│   └── utils.py          # Utility functions
├── models/               # Pre-trained models directory
└── myenv/                # Virtual environment (ignore in version control)
```

## Technologies Used

- **Streamlit**: Web app framework
- **Selenium**: Web scraping
- **Transformers**: NLP models for sentiment analysis
- **Groq API**: AI chatbot functionality
- **Matplotlib & WordCloud**: Data visualization
- **Pandas**: Data manipulation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
