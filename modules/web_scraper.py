"""
Web Scraper Module for Veritas News Analysis
Extracts article content from news URLs using newspaper3k and BeautifulSoup
"""

import requests
from newspaper import Article
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
import time

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_article(self, url):
        """
        Primary method to extract article content from a URL
        First tries newspaper3k, falls back to BeautifulSoup if needed
        """
        logger.info(f"Starting scrape for URL: {url}")
        
        # Method 1: Try newspaper3k (optimized for news sites)
        article_data = self._scrape_with_newspaper(url)
        
        if article_data and article_data.get('content'):
            logger.info("Successfully scraped using newspaper3k")
            return article_data
        
        # Method 2: Fallback to BeautifulSoup
        logger.info("Newspaper3k failed, trying BeautifulSoup fallback")
        article_data = self._scrape_with_beautifulsoup(url)
        
        if article_data and article_data.get('content'):
            logger.info("Successfully scraped using BeautifulSoup")
            return article_data
        
        logger.error("Both scraping methods failed")
        return None
    
    def _scrape_with_newspaper(self, url):
        """Use newspaper3k library for news-specific extraction"""
        try:
            article = Article(url)
            article.download()
            
            # Add small delay to be respectful to servers
            time.sleep(1)
            
            article.parse()
            
            # Extract domain for source identification
            domain = urlparse(url).netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return {
                'title': article.title or 'No title found',
                'content': article.text or '',
                'source_domain': domain,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                'authors': article.authors,
                'url': url,
                'method': 'newspaper3k'
            }
            
        except Exception as e:
            logger.error(f"Newspaper3k scraping failed: {str(e)}")
            return None
    
    def _scrape_with_beautifulsoup(self, url):
        """Fallback method using BeautifulSoup for general web scraping"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract main content
            content = self._extract_content(soup)
            
            # Extract domain
            domain = urlparse(url).netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return {
                'title': title or 'No title found',
                'content': content or '',
                'source_domain': domain,
                'publish_date': None,
                'authors': [],
                'url': url,
                'method': 'beautifulsoup'
            }
            
        except Exception as e:
            logger.error(f"BeautifulSoup scraping failed: {str(e)}")
            return None
    
    def _extract_title(self, soup):
        """Extract article title from HTML"""
        # Try multiple title selectors
        title_selectors = [
            'h1',
            '.headline',
            '.title',
            '[data-testid="headline"]',
            '.entry-title',
            '.post-title'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem and title_elem.get_text(strip=True):
                return title_elem.get_text(strip=True)
        
        # Fallback to page title
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else None
    
    def _extract_content(self, soup):
        """Extract main article content from HTML"""
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            element.decompose()
        
        # Try content-specific selectors first
        content_selectors = [
            '[data-testid="ArticleBody"]',
            '.article-body',
            '.entry-content',
            '.post-content',
            '.content',
            'article',
            '.story-body',
            '.article-content'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Get all paragraph text
                paragraphs = content_elem.find_all(['p', 'div'], recursive=True)
                content_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                if len(content_text) > 100:  # Minimum content length
                    return self._clean_content(content_text)
        
        # Fallback: extract all paragraphs from body
        paragraphs = soup.find_all('p')
        if paragraphs:
            content_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            return self._clean_content(content_text)
        
        return None
    
    def _clean_content(self, content):
        """Clean and filter extracted content"""
        if not content:
            return None
        
        # Remove excessive whitespace
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Filter out likely navigation/footer content
        filtered_lines = []
        skip_phrases = [
            'sign up',
            'subscribe',
            'newsletter',
            'follow us',
            'share this',
            'advertisement',
            'more stories'
        ]
        
        for line in lines:
            if len(line) > 20 and not any(phrase in line.lower() for phrase in skip_phrases):
                filtered_lines.append(line)
        
        return '\n\n'.join(filtered_lines)
    
    def is_valid_news_url(self, url):
        """Check if URL appears to be from a news website"""
        try:
            domain = urlparse(url).netloc.lower()
            
            # Common news domains patterns
            news_indicators = [
                'news', 'times', 'post', 'herald', 'tribune', 'journal', 
                'guardian', 'telegraph', 'reuters', 'bbc', 'cnn', 'nbc',
                'abc', 'cbs', 'fox', 'npr', 'pbs', 'economist', 'wsj'
            ]
            
            return any(indicator in domain for indicator in news_indicators)
            
        except Exception:
            return False