# Veritas News Credibility Analysis System

![Veritas Logo](https://img.shields.io/badge/Veritas-News%20Analysis-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-red)
![AI](https://img.shields.io/badge/AI-BART%20%2B%20RoBERTa-orange)

A comprehensive AI-powered system for analyzing news articles to determine credibility, emotional tone, and provide intelligent summaries. Built with cutting-edge NLP models and a robust credibility scoring algorithm.

## 🚀 Features

### Core Analysis Capabilities
- **📊 Credibility Scoring**: Multi-factor analysis combining source reputation with content quality indicators
- **🤖 AI Summarization**: BART model generates concise, intelligent summaries
- **😊 Emotion Detection**: RoBERTa model analyzes emotional tone (positive/negative/neutral)
- **🕷️ Smart Web Scraping**: Dual-layer extraction using newspaper3k + BeautifulSoup
- **📈 Visual Analytics**: Interactive charts and comprehensive breakdowns

### Source Database
- **50+ News Sources**: Pre-rated credibility database covering major outlets
- **Tier System**: 4-tier credibility classification (Highly Credible to Mixed)
- **Regular Updates**: Continuously updated source reputation scores
- **Coverage**: Reuters, BBC, CNN, Fox News, NYT, WSJ, and many more

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python + Flask
- **AI Models**: 
  - BART (facebook/bart-large-cnn) for summarization
  - RoBERTa (cardiffnlp/twitter-roberta-base-emotion) for emotion detection
- **Web Scraping**: newspaper3k + BeautifulSoup4
- **Frontend**: HTML5 + CSS3 + JavaScript + Chart.js
- **Data Processing**: NumPy, NLTK, transformers

### System Components
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Scraper   │───▶│   AI Analyzer    │───▶│ Credibility     │
│                 │    │                  │    │ Scorer          │
│ • newspaper3k   │    │ • BART Summary   │    │                 │
│ • BeautifulSoup │    │ • RoBERTa Emotion│    │ • Source DB     │
│ • Fallback      │    │ • Fallbacks      │    │ • Content Eval  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- 4GB+ RAM (for AI models)
- Internet connection (for web scraping)

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd veritas

# Install dependencies
pip install -r requirements.txt

# Download required NLTK data (first time only)
python -c "import nltk; nltk.download('punkt')"

# Run the application
python app.py
```

### Environment Setup
```bash
# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## 🚀 Usage

### Web Interface
1. Start the application: `python app.py`
2. Open browser to `http://localhost:5000`
3. Enter a news article URL
4. Get comprehensive analysis in seconds

### API Endpoints

#### Analyze Article
```http
POST /api/analyze
Content-Type: application/json

{
    "url": "https://example.com/news-article"
}
```

#### Response Format
```json
{
    "article": {
        "title": "Article Title",
        "source_domain": "example.com",
        "url": "https://example.com/news-article",
        "content_preview": "Article preview..."
    },
    "analysis": {
        "credibility": {
            "final_score": 85.2,
            "confidence": 0.87,
            "interpretation": {
                "level": "High Credibility",
                "description": "Reliable source with good practices"
            },
            "breakdown": {
                "source_reputation": {"score": 12.6, "source_name": "BBC"},
                "article_length": {"score": 10, "word_count": 800},
                "citations": {"score": 9, "citation_count": 3}
            }
        },
        "emotion": {
            "emotion": "neutral",
            "confidence": 0.82,
            "method": "roberta_ai"
        },
        "summary": "AI-generated article summary..."
    }
}
```

#### Get Sources Database
```http
GET /api/sources
```

## 🎯 Credibility Scoring Algorithm

### Scoring Components
| Factor | Weight | Description |
|--------|--------|-------------|
| **Base Score** | 50% | Neutral starting point |
| **Source Reputation** | ±30% | Known source credibility rating |
| **Article Length** | ±10% | Comprehensive vs. brief coverage |
| **Citations** | +15% | Source attribution indicators |
| **Factual Content** | +10% | Data, numbers, official references |
| **Emotional Language** | -10% | Penalty for sensational wording |

### Source Tiers
- **Tier 1 (85-95%)**: Reuters, BBC, AP, NPR, PBS
- **Tier 2 (75-85%)**: NYT, WashPost, WSJ, Guardian, Economist  
- **Tier 3 (65-75%)**: CNN, NBC, ABC, CBS, Time
- **Tier 4 (55-65%)**: Fox News, MSNBC, NY Post, HuffPost

### Content Analysis Indicators

#### ✅ Positive Signals
- **Citations**: "according to", "study shows", "expert says"
- **Facts**: dates, percentages, official names, statistics
- **Length**: 500+ words indicates thorough coverage

#### ❌ Negative Signals  
- **Emotional words**: "shocking", "unbelievable", "outrageous"
- **Brief articles**: <200 words suggests incomplete coverage
- **Missing sources**: claims without attribution

## 📊 Sample Analysis

### Input
```
URL: https://bbc.com/news/climate-change-study
```

### Output
```
Credibility Score: 84.6%
├── Base Score: +50.0%
├── Source (BBC): +12.6%
├── Length (800 words): +10.0%
├── Citations (3 found): +9.0%
├── Facts (5 indicators): +5.0%
└── Emotional (-1 word): -2.0%

Emotion: Neutral (82% confidence)
Summary: "Climate researchers report significant temperature increases..."
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional configurations
export SECRET_KEY="your-secret-key"
export DEBUG=False
export PORT=5000
```

### Model Configuration
Models are loaded automatically on first use. For custom configurations:

```python
# In modules/ai_analyzer.py
self.summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",  # Change model here
    device=0 if torch.cuda.is_available() else -1
)
```

## 📝 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main web interface |
| `POST` | `/api/analyze` | Analyze news article |
| `GET` | `/api/sources` | Get source database |
| `GET` | `/api/health` | Health check |

### Error Handling
All endpoints return structured error responses:
```json
{
    "error": "Description of error",
    "code": 400,
    "timestamp": "2026-01-07T12:00:00Z"
}
```

## 🧪 Testing

### Run Sample Analysis
```bash
# Test with a known article
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news"}'
```

### Validate Installation
```bash
# Check health endpoint
curl http://localhost:5000/api/health
```

## 📚 Example Use Cases

### 1. Fact Checking
Quickly assess the credibility of news articles shared on social media

### 2. Media Literacy Education
Help students understand credibility indicators in journalism

### 3. Research Validation
Verify source quality for academic or professional research

### 4. Content Curation
Filter high-quality articles for news aggregation platforms

## ⚠️ Limitations

### What We DON'T Do
- ❌ Real-time fact-checking of specific claims
- ❌ Political bias assessment (we focus on factual accuracy)
- ❌ Individual journalist reputation tracking
- ❌ Content verification against external databases

### Known Issues
- AI models require significant RAM (4GB+ recommended)
- Some websites may block automated scraping
- Summarization quality varies with article complexity
- Emotion detection trained primarily on English text

## 🔒 Privacy & Ethics

### Data Handling
- **No Storage**: Articles are processed in memory only
- **No Tracking**: No user behavior or article analysis stored
- **Respectful Scraping**: Implements delays and respects robots.txt

### Ethical Considerations
- Tool is designed to supplement, not replace, critical thinking
- Source database aims for objectivity but reflects editorial choices
- Results should be considered alongside other verification methods

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black modules/ *.py

# Lint code
flake8 modules/ *.py
```

### Adding New Sources
Update `modules/source_database.py`:
```python
new_sources = {
    'example.com': {
        'name': 'Example News',
        'credibility': 75,
        'tier': 3,
        'description': 'Regional news outlet'
    }
}
```

## 📞 Support

### Common Issues
1. **Model Loading Errors**: Ensure 4GB+ RAM available
2. **Scraping Failures**: Some sites block automated access
3. **Slow Performance**: First AI model load takes time

### Getting Help
- Check the logs for detailed error messages
- Ensure all requirements are properly installed
- Verify internet connectivity for both scraping and model downloads

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hugging Face** for BART and RoBERTa models
- **newspaper3k** for news extraction capabilities
- **Chart.js** for visualization components
- **Media research organizations** for credibility benchmarks

---

**Veritas** - *"Truth through Analysis"* 

Built for journalists, researchers, educators, and anyone who values informed decision-making in our information age.