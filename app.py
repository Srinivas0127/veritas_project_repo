#!/usr/bin/env python3
"""
Veritas News Credibility Analysis System
Main Flask application entry point
"""

from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime

# Import our custom modules
from modules.web_scraper import WebScraper
from modules.ai_analyzer_simple import AIAnalyzer
from modules.credibility_scorer import CredibilityScorer
from modules.source_database import SourceDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'veritas-news-analysis-2026')

# Initialize components
web_scraper = WebScraper()
ai_analyzer = AIAnalyzer()
credibility_scorer = CredibilityScorer()
source_db = SourceDatabase()

@app.route('/')
def index():
    """Main page for the Veritas news analysis tool"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_news():
    """
    Main API endpoint for analyzing news articles
    Expects: {'url': 'news_article_url'}
    Returns: Complete analysis including credibility, emotion, and summary
    """
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
    sources = source_db.get_all_sources()
    return jsonify(sources)

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
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)