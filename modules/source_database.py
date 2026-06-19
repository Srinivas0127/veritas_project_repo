"""
Source Database Module for Veritas News Analysis
Maintains credibility ratings for 50+ news sources
"""

import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class SourceDatabase:
    def __init__(self):
        self.sources = self._load_source_database()
    
    def _load_source_database(self):
        """Load the news source credibility database"""
        # Tier 1: Highly Credible (85-95%)
        tier1_sources = {
            'reuters.com': {'name': 'Reuters', 'credibility': 95, 'tier': 1, 'description': 'International wire service, fact-focused'},
            'apnews.com': {'name': 'Associated Press', 'credibility': 93, 'tier': 1, 'description': 'Non-profit news cooperative'},
            'ap.org': {'name': 'Associated Press', 'credibility': 93, 'tier': 1, 'description': 'Non-profit news cooperative'},
            'bbc.com': {'name': 'BBC', 'credibility': 92, 'tier': 1, 'description': 'Public broadcaster with editorial standards'},
            'bbc.co.uk': {'name': 'BBC', 'credibility': 92, 'tier': 1, 'description': 'Public broadcaster with editorial standards'},
            'npr.org': {'name': 'NPR', 'credibility': 90, 'tier': 1, 'description': 'Public radio with journalistic integrity'},
            'pbs.org': {'name': 'PBS', 'credibility': 88, 'tier': 1, 'description': 'Public broadcasting service'},
        }
        
        # Tier 2: Very Credible (75-85%)
        tier2_sources = {
            'nytimes.com': {'name': 'New York Times', 'credibility': 83, 'tier': 2, 'description': 'Established newspaper with fact-checking'},
            'washingtonpost.com': {'name': 'Washington Post', 'credibility': 82, 'tier': 2, 'description': 'Major daily with investigative journalism'},
            'wsj.com': {'name': 'Wall Street Journal', 'credibility': 81, 'tier': 2, 'description': 'Business-focused with high standards'},
            'theguardian.com': {'name': 'The Guardian', 'credibility': 80, 'tier': 2, 'description': 'International newspaper'},
            'economist.com': {'name': 'The Economist', 'credibility': 85, 'tier': 2, 'description': 'Weekly news magazine'},
            'usatoday.com': {'name': 'USA Today', 'credibility': 78, 'tier': 2, 'description': 'National newspaper'},
            'latimes.com': {'name': 'Los Angeles Times', 'credibility': 79, 'tier': 2, 'description': 'Major regional newspaper'},
            'chicagotribune.com': {'name': 'Chicago Tribune', 'credibility': 77, 'tier': 2, 'description': 'Regional newspaper'},
        }
        
        # Tier 3: Generally Credible (65-75%)
        tier3_sources = {
            'cnn.com': {'name': 'CNN', 'credibility': 72, 'tier': 3, 'description': 'Cable news network'},
            'nbcnews.com': {'name': 'NBC News', 'credibility': 71, 'tier': 3, 'description': 'Broadcast network news'},
            'abcnews.go.com': {'name': 'ABC News', 'credibility': 70, 'tier': 3, 'description': 'Television network news'},
            'cbsnews.com': {'name': 'CBS News', 'credibility': 69, 'tier': 3, 'description': 'Broadcast journalism'},
            'time.com': {'name': 'Time', 'credibility': 74, 'tier': 3, 'description': 'News magazine'},
            'newsweek.com': {'name': 'Newsweek', 'credibility': 68, 'tier': 3, 'description': 'News magazine'},
            'politico.com': {'name': 'Politico', 'credibility': 75, 'tier': 3, 'description': 'Political news'},
            'thehill.com': {'name': 'The Hill', 'credibility': 73, 'tier': 3, 'description': 'Political news'},
        }
        
        # Tier 4: Mixed Credibility (55-65%)
        tier4_sources = {
            'foxnews.com': {'name': 'Fox News', 'credibility': 60, 'tier': 4, 'description': 'Cable news with editorial slant'},
            'msnbc.com': {'name': 'MSNBC', 'credibility': 58, 'tier': 4, 'description': 'Cable news with political perspective'},
            'nypost.com': {'name': 'New York Post', 'credibility': 55, 'tier': 4, 'description': 'Tabloid-style newspaper'},
            'dailymail.co.uk': {'name': 'Daily Mail', 'credibility': 52, 'tier': 4, 'description': 'UK tabloid'},
            'huffpost.com': {'name': 'HuffPost', 'credibility': 62, 'tier': 4, 'description': 'Digital news and opinion'},
            'buzzfeed.com': {'name': 'BuzzFeed News', 'credibility': 57, 'tier': 4, 'description': 'Digital media company'},
        }
        
        # Additional credible sources
        additional_sources = {
            'aljazeera.com': {'name': 'Al Jazeera', 'credibility': 76, 'tier': 3, 'description': 'International news network'},
            'dw.com': {'name': 'Deutsche Welle', 'credibility': 84, 'tier': 2, 'description': 'German international broadcaster'},
            'france24.com': {'name': 'France 24', 'credibility': 82, 'tier': 2, 'description': 'French international news'},
            'axios.com': {'name': 'Axios', 'credibility': 79, 'tier': 2, 'description': 'Digital news startup'},
            'propublica.org': {'name': 'ProPublica', 'credibility': 91, 'tier': 1, 'description': 'Nonprofit investigative journalism'},
            'factcheck.org': {'name': 'FactCheck.org', 'credibility': 94, 'tier': 1, 'description': 'Fact-checking organization'},
            'snopes.com': {'name': 'Snopes', 'credibility': 89, 'tier': 1, 'description': 'Fact-checking website'},
            'politifact.com': {'name': 'PolitiFact', 'credibility': 87, 'tier': 1, 'description': 'Political fact-checking'},
        }
        
        # Combine all sources
        all_sources = {}
        all_sources.update(tier1_sources)
        all_sources.update(tier2_sources)
        all_sources.update(tier3_sources)
        all_sources.update(tier4_sources)
        all_sources.update(additional_sources)
        
        logger.info(f"Loaded {len(all_sources)} news sources into database")
        return all_sources
    
    def get_source_credibility(self, url_or_domain):
        """Get credibility score for a news source from URL or domain"""
        try:
            # Extract domain from URL if needed
            if url_or_domain.startswith('http'):
                domain = urlparse(url_or_domain).netloc.lower()
            else:
                domain = url_or_domain.lower()
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Direct match
            if domain in self.sources:
                source_info = self.sources[domain]
                logger.info(f"Found source: {source_info['name']} (credibility: {source_info['credibility']}%)")
                return source_info
            
            # Try subdomain variations
            for known_domain in self.sources:
                if domain.endswith(known_domain) or known_domain.endswith(domain):
                    source_info = self.sources[known_domain]
                    logger.info(f"Found source via subdomain match: {source_info['name']}")
                    return source_info
            
            # Unknown source
            logger.info(f"Unknown source domain: {domain}")
            return {
                'name': f'Unknown ({domain})',
                'credibility': 50,  # Neutral score for unknown sources
                'tier': 5,
                'description': 'Source not in database'
            }
            
        except Exception as e:
            logger.error(f"Error getting source credibility: {str(e)}")
            return {
                'name': 'Error',
                'credibility': 50,
                'tier': 5,
                'description': 'Unable to determine source'
            }
    
    def get_all_sources(self):
        """Get all sources organized by tier"""
        sources_by_tier = {
            1: [],  # Highly Credible
            2: [],  # Very Credible
            3: [],  # Generally Credible
            4: [],  # Mixed Credibility
            5: []   # Unknown/Low Credibility
        }
        
        for domain, info in self.sources.items():
            tier = info.get('tier', 5)
            sources_by_tier[tier].append({
                'domain': domain,
                'name': info['name'],
                'credibility': info['credibility'],
                'description': info['description']
            })
        
        # Sort each tier by credibility score (highest first)
        for tier in sources_by_tier:
            sources_by_tier[tier].sort(key=lambda x: x['credibility'], reverse=True)
        
        return {
            'total_sources': len(self.sources),
            'tiers': {
                '1_highly_credible': {
                    'description': 'Highly Credible (85-95%)',
                    'sources': sources_by_tier[1]
                },
                '2_very_credible': {
                    'description': 'Very Credible (75-85%)',
                    'sources': sources_by_tier[2]
                },
                '3_generally_credible': {
                    'description': 'Generally Credible (65-75%)',
                    'sources': sources_by_tier[3]
                },
                '4_mixed_credibility': {
                    'description': 'Mixed Credibility (55-65%)',
                    'sources': sources_by_tier[4]
                }
            }
        }
    
    def is_known_source(self, domain):
        """Check if a domain is in our source database"""
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.lower() in self.sources
    
    def get_tier_description(self, tier):
        """Get description for credibility tier"""
        descriptions = {
            1: "Highly Credible - International wire services, public broadcasters, and established fact-checkers",
            2: "Very Credible - Major newspapers and news magazines with strong editorial standards",
            3: "Generally Credible - Mainstream broadcast and cable news networks",
            4: "Mixed Credibility - Sources with known editorial bias or tabloid characteristics",
            5: "Unknown/Unrated - Sources not yet evaluated in our database"
        }
        return descriptions.get(tier, "Unknown tier")