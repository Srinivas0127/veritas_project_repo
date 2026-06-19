#!/usr/bin/env python3
"""
Veritas Server with Better Error Handling and Debugging
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import logging
from datetime import datetime

# Import our custom modules
from modules.web_scraper import WebScraper
from modules.ai_analyzer_simple import AIAnalyzer
from modules.credibility_scorer import CredibilityScorer
from modules.source_database import SourceDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'veritas-news-analysis-2026')

# Initialize components
try:
    web_scraper = WebScraper()
    ai_analyzer = AIAnalyzer()
    credibility_scorer = CredibilityScorer()
    source_db = SourceDatabase()
    logger.info("All modules initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize modules: {e}")
    raise

@app.route('/')
def index():
    """Main page for the Veritas news analysis tool"""
    try:
        logger.info("Serving main page")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving main page: {e}")
        return f"<h1>Veritas News Analysis</h1><p>Error loading page: {e}</p><p>Static files path: {app.static_folder}</p><p>Templates path: {app.template_folder}</p>", 500

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/test')
def test():
    """Simple test page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Veritas Test</title>
        <style>
            body { font-family: Arial; padding: 20px; background: white; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
            .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Veritas Test Page</h1>
            <div class="status success">✅ Server is running correctly!</div>
            <div class="status info">📡 Access the main interface at: <a href="/">Main Page</a></div>
            <div class="status info">🔧 API Health Check: <a href="/api/health">Health Status</a></div>
            <p><strong>If you see this page, the server is working!</strong></p>
        </div>
    </body>
    </html>
    """

@app.route('/api/analyze', methods=['POST'])
def analyze_news():
    """Main API endpoint for analyzing news articles"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        logger.info(f"Starting analysis for URL: {url}")
        
        # Step 1: Scrape article content
        article_data = web_scraper.scrape_article(url)
        if not article_data:
            return jsonify({'error': 'Failed to extract article content'}), 400
        
        # Step 2: AI Analysis
        summary = ai_analyzer.summarize_text(article_data['content'])
        emotion = ai_analyzer.detect_emotion(article_data['content'])
        
        # Step 3: Credibility Analysis
        credibility_score = credibility_scorer.calculate_credibility(
            url=url,
            content=article_data['content'],
            title=article_data.get('title', ''),
            source_domain=article_data.get('source_domain', '')
        )
        
        # Compile results
        results = {
            'article': {
                'url': url,
                'title': article_data.get('title', 'No title found'),
                'source_domain': article_data.get('source_domain', 'Unknown'),
                'publish_date': article_data.get('publish_date'),
                'content_preview': article_data['content'][:300] + '...' if len(article_data['content']) > 300 else article_data['content']
            },
            'analysis': {
                'summary': summary,
                'emotion': emotion,
                'credibility': credibility_score
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Analysis complete. Credibility score: {credibility_score['final_score']}")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/sources')
def get_sources():
    """Get information about known news sources and their credibility ratings"""
    try:
        sources = source_db.get_all_sources()
        return jsonify(sources)
    except Exception as e:
        logger.error(f"Sources endpoint failed: {e}")
        return jsonify({'error': 'Failed to load sources'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'web_scraper': 'operational',
            'ai_analyzer': 'operational', 
            'credibility_scorer': 'operational',
            'source_database': 'operational'
        }
    })

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.url}")
    try:
        return render_template('404.html'), 404
    except:
        return "<h1>404 - Page Not Found</h1><p>The page you're looking for doesn't exist.</p>", 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    try:
        return render_template('500.html'), 500
    except:
        return "<h1>500 - Internal Server Error</h1><p>Something went wrong on our end.</p>", 500

if __name__ == '__main__':
    print("🛡️  Starting Veritas News Analysis System")
    print(f"📁 Static folder: {app.static_folder}")
    print(f"📄 Template folder: {app.template_folder}")
    print(f"📡 Server will be available at: http://localhost:8080")
    
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=True,
        use_reloader=False
    )