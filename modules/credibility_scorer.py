"""
Credibility Scorer Module for Veritas News Analysis
Calculates credibility scores based on source reputation and content analysis
"""

import logging
import re
from urllib.parse import urlparse
from modules.source_database import SourceDatabase

logger = logging.getLogger(__name__)

class CredibilityScorer:
    def __init__(self):
        self.source_db = SourceDatabase()
        
        # Content analysis weights (must sum to 100%)
        self.weights = {
            'source_reputation': 30,  # 30% weight for source credibility
            'article_length': 10,     # 10% weight for article length
            'citations': 15,          # 15% weight for source citations
            'factual_content': 10,    # 10% weight for factual indicators
            'emotional_language': -10, # -10% penalty for sensational language
            'base_score': 50          # 50% base neutral score
        }
    
    def calculate_credibility(self, url, content, title="", source_domain=""):
        """
        Main method to calculate credibility score
        Returns detailed scoring breakdown
        """
        logger.info(f"Calculating credibility for: {url}")
        
        # Get source reputation
        source_info = self.source_db.get_source_credibility(url)
        
        # Calculate individual factors
        source_score = self._calculate_source_score(source_info)
        length_score = self._calculate_length_score(content)
        citation_score = self._calculate_citation_score(content)
        factual_score = self._calculate_factual_score(content)
        emotional_penalty = self._calculate_emotional_penalty(content, title)
        
        # Calculate final score
        final_score = (
            self.weights['base_score'] +
            source_score +
            length_score +
            citation_score +
            factual_score +
            emotional_penalty
        )
        
        # Ensure score is between 0-100
        final_score = max(0, min(100, final_score))
        
        # Determine confidence level
        confidence = self._calculate_confidence(source_info, len(content))
        
        result = {
            'final_score': round(final_score, 1),
            'confidence': confidence,
            'breakdown': {
                'base_score': self.weights['base_score'],
                'source_reputation': {
                    'score': round(source_score, 1),
                    'weight': f"{self.weights['source_reputation']}%",
                    'source_name': source_info['name'],
                    'source_credibility': source_info['credibility'],
                    'tier': source_info['tier']
                },
                'article_length': {
                    'score': round(length_score, 1),
                    'weight': f"{self.weights['article_length']}%",
                    'word_count': len(content.split()),
                    'category': self._get_length_category(content)
                },
                'citations': {
                    'score': round(citation_score, 1),
                    'weight': f"{self.weights['citations']}%",
                    'citation_count': self._count_citations(content)
                },
                'factual_content': {
                    'score': round(factual_score, 1),
                    'weight': f"{self.weights['factual_content']}%",
                    'factual_indicators': self._count_factual_indicators(content)
                },
                'emotional_language': {
                    'score': round(emotional_penalty, 1),
                    'weight': f"{self.weights['emotional_language']}% (penalty)",
                    'emotional_words': self._count_emotional_words(content, title)
                }
            },
            'interpretation': self._interpret_score(final_score),
            'recommendation': self._get_recommendation(final_score, confidence)
        }
        
        logger.info(f"Credibility analysis complete. Final score: {final_score}")
        return result
    
    def _calculate_source_score(self, source_info):
        """Calculate score contribution from source reputation"""
        source_credibility = source_info['credibility']
        # Convert source credibility (0-100) to weighted contribution
        return (source_credibility - 50) * self.weights['source_reputation'] / 100
    
    def _calculate_length_score(self, content):
        """Calculate score based on article length"""
        word_count = len(content.split())
        
        if word_count >= 500:
            return self.weights['article_length']  # +10%
        elif word_count >= 200:
            return self.weights['article_length'] / 2  # +5%
        else:
            return -self.weights['article_length']  # -10%
    
    def _calculate_citation_score(self, content):
        """Calculate score based on source citations"""
        citation_count = self._count_citations(content)
        
        # Scale citation score (max +15%)
        if citation_count >= 5:
            return self.weights['citations']
        elif citation_count >= 3:
            return self.weights['citations'] * 0.8
        elif citation_count >= 1:
            return self.weights['citations'] * 0.6
        else:
            return 0
    
    def _calculate_factual_score(self, content):
        """Calculate score based on factual content indicators"""
        factual_count = self._count_factual_indicators(content)
        
        # Scale factual score (max +10%)
        if factual_count >= 8:
            return self.weights['factual_content']
        elif factual_count >= 5:
            return self.weights['factual_content'] * 0.8
        elif factual_count >= 3:
            return self.weights['factual_content'] * 0.5
        else:
            return 0
    
    def _calculate_emotional_penalty(self, content, title):
        """Calculate penalty for emotional/sensational language"""
        emotional_count = self._count_emotional_words(content, title)
        
        # Scale emotional penalty (max -10%)
        if emotional_count >= 5:
            return self.weights['emotional_language']  # Full penalty
        elif emotional_count >= 3:
            return self.weights['emotional_language'] * 0.8
        elif emotional_count >= 1:
            return self.weights['emotional_language'] * 0.5
        else:
            return 0
    
    def _count_citations(self, content):
        """Count source citation indicators"""
        citation_patterns = [
            r'according to',
            r'said [A-Z][a-z]+',  # "said Smith"
            r'study (?:shows|found|revealed)',
            r'research (?:shows|indicates|suggests)',
            r'data (?:shows|indicates|suggests)',
            r'report(?:ed|s) (?:by|from)',
            r'expert(?:s)? (?:say|said|believe)',
            r'official(?:s)? (?:say|said|told)',
            r'source(?:s)? (?:say|said|told)',
            r'survey (?:found|shows|indicates)',
            r'analysis (?:shows|found|reveals)',
            r'statistics (?:show|indicate)'
        ]
        
        content_lower = content.lower()
        citation_count = 0
        
        for pattern in citation_patterns:
            matches = re.findall(pattern, content_lower)
            citation_count += len(matches)
        
        return citation_count
    
    def _count_factual_indicators(self, content):
        """Count factual content indicators"""
        factual_patterns = [
            r'\d+(?:\.\d+)?%',  # Percentages
            r'\d{4}',  # Years
            r'(?:january|february|march|april|may|june|july|august|september|october|november|december)',  # Months
            r'\$\d+(?:,\d{3})*(?:\.\d{2})?',  # Dollar amounts
            r'\d+(?:,\d{3})*\s+(?:people|individuals|residents|citizens)',  # Population figures
            r'(?:government|department|agency|organization|company|corporation)',  # Official entities
            r'(?:president|minister|senator|representative|governor|mayor)',  # Official titles
            r'\d+(?:st|nd|rd|th)',  # Dates with ordinals
            r'(?:morning|afternoon|evening|tonight|yesterday|today)',  # Time references
        ]
        
        content_lower = content.lower()
        factual_count = 0
        
        for pattern in factual_patterns:
            matches = re.findall(pattern, content_lower)
            factual_count += len(matches)
        
        return min(factual_count, 15)  # Cap to prevent over-counting
    
    def _count_emotional_words(self, content, title):
        """Count sensational/emotional language"""
        emotional_words = [
            'shocking', 'unbelievable', 'incredible', 'amazing', 'outrageous',
            'scandal', 'explosive', 'devastating', 'miraculous', 'sensational',
            'breakthrough', 'revolutionary', 'stunning', 'extraordinary', 'bizarre',
            'horrific', 'terrifying', 'mind-blowing', 'jaw-dropping', 'unthinkable',
            'exclusive', 'bombshell', 'urgent', 'breaking', 'crisis'
        ]
        
        text = (content + " " + title).lower()
        emotional_count = 0
        
        for word in emotional_words:
            if word in text:
                emotional_count += text.count(word)
        
        return emotional_count
    
    def _get_length_category(self, content):
        """Get article length category"""
        word_count = len(content.split())
        
        if word_count >= 500:
            return "Comprehensive (500+ words)"
        elif word_count >= 200:
            return "Adequate (200-500 words)"
        else:
            return "Brief (<200 words)"
    
    def _calculate_confidence(self, source_info, content_length):
        """Calculate confidence in the credibility assessment"""
        confidence = 0.5  # Base confidence
        
        # Higher confidence for known sources
        if source_info['tier'] <= 3:
            confidence += 0.3
        elif source_info['tier'] == 4:
            confidence += 0.2
        
        # Higher confidence for longer articles
        if content_length > 1000:
            confidence += 0.2
        elif content_length > 500:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _interpret_score(self, score):
        """Provide interpretation of credibility score"""
        if score >= 80:
            return {
                'level': 'High Credibility',
                'description': 'This article comes from a reliable source and demonstrates good journalistic practices.',
                'color': 'green'
            }
        elif score >= 65:
            return {
                'level': 'Good Credibility',
                'description': 'This article is generally trustworthy with some quality indicators.',
                'color': 'lightgreen'
            }
        elif score >= 50:
            return {
                'level': 'Moderate Credibility',
                'description': 'This article has mixed credibility indicators. Verify important claims.',
                'color': 'yellow'
            }
        elif score >= 35:
            return {
                'level': 'Low Credibility',
                'description': 'This article shows concerning signs. Be cautious and seek verification.',
                'color': 'orange'
            }
        else:
            return {
                'level': 'Very Low Credibility',
                'description': 'This article has multiple red flags. Treat claims with high skepticism.',
                'color': 'red'
            }
    
    def _get_recommendation(self, score, confidence):
        """Provide actionable recommendation based on score and confidence"""
        if score >= 75 and confidence >= 0.8:
            return "This appears to be a reliable news article from a credible source."
        elif score >= 65 and confidence >= 0.7:
            return "This article is generally trustworthy, but consider cross-referencing key facts."
        elif score >= 50:
            return "Exercise caution with this article. Verify claims through additional reliable sources."
        elif score >= 35:
            return "This article shows significant credibility concerns. Seek verification from multiple trusted sources."
        else:
            return "This article has major credibility issues. Do not rely on it without substantial verification."