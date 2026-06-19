"""
AI Analyzer Module for Veritas News Analysis - Simplified Version
Handles text summarization and emotion detection with fallback implementations
"""

import logging
import re
import random

logger = logging.getLogger(__name__)

class AIAnalyzer:
    def __init__(self):
        self.summarizer = None
        self.emotion_analyzer = None
        
        logger.info("AI Analyzer initialized with fallback implementations")
        logger.warning("Full AI models (BART/RoBERTa) not available - using simplified algorithms")
    
    def summarize_text(self, text, max_length=150, min_length=30):
        """
        Generate summary using extractive summarization
        Full AI models can be enabled by installing torch and transformers properly
        """
        if not text or len(text.strip()) < 50:
            return "Text too short to summarize"
        
        logger.info("Using extractive summarization (AI models not available)")
        return self._extractive_summary(text, max_sentences=3)
    
    def detect_emotion(self, text):
        """
        Detect emotion using keyword-based analysis
        Full AI models can be enabled by installing torch and transformers properly
        """
        if not text or len(text.strip()) < 10:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'method': 'insufficient_text'
            }
        
        logger.info("Using keyword-based emotion detection (AI models not available)")
        return self._keyword_emotion_detection(text)
    
    def _extractive_summary(self, text, max_sentences=3):
        """Extractive summarization using first few meaningful sentences"""
        try:
            sentences = self._split_sentences(text)
            
            # Filter out very short sentences and likely navigation text
            meaningful_sentences = []
            for sentence in sentences:
                if (len(sentence) > 20 and 
                    not any(skip_word in sentence.lower() for skip_word in 
                           ['click here', 'read more', 'subscribe', 'sign up', 'follow us', 'advertisement'])):
                    meaningful_sentences.append(sentence.strip())
            
            # Take first few meaningful sentences
            summary_sentences = meaningful_sentences[:max_sentences]
            
            if summary_sentences:
                return ' '.join(summary_sentences)
            else:
                return "Unable to generate meaningful summary from this content."
                
        except Exception as e:
            logger.error(f"Extractive summarization failed: {str(e)}")
            return "Summary generation failed"
    
    def _split_sentences(self, text):
        """Simple sentence splitting"""
        # Split on sentence endings
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _keyword_emotion_detection(self, text):
        """Enhanced keyword-based emotion detection"""
        text_lower = text.lower()
        
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
            'positive', 'success', 'achievement', 'victory', 'win', 'progress',
            'improve', 'benefit', 'advantage', 'opportunity', 'hope', 'optimistic',
            'breakthrough', 'celebrate', 'joy', 'happy', 'pleased', 'satisfied',
            'thrilled', 'excited', 'brilliant', 'outstanding', 'remarkable'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'fail', 'failure',
            'crisis', 'disaster', 'tragedy', 'problem', 'issue', 'concern',
            'worry', 'fear', 'angry', 'sad', 'disappointed', 'frustrated',
            'devastating', 'shocking', 'outrageous', 'alarming', 'troubling',
            'dangerous', 'threat', 'risk', 'damage', 'harm', 'loss', 'decline'
        ]
        
        neutral_indicators = [
            'report', 'announce', 'state', 'according', 'data', 'research',
            'study', 'analysis', 'official', 'government', 'company', 'said',
            'meeting', 'discussion', 'plan', 'proposal', 'policy', 'decision'
        ]
        
        # Count occurrences
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        neutral_count = sum(1 for word in neutral_indicators if word in text_lower)
        
        # Calculate total signal strength
        total_signals = positive_count + negative_count + neutral_count
        
        if total_signals == 0:
            # No clear indicators, classify as neutral
            return {
                'emotion': 'neutral',
                'confidence': 0.5,
                'positive_signals': 0,
                'negative_signals': 0,
                'neutral_signals': 0,
                'method': 'keyword_fallback'
            }
        
        # Determine emotion based on strongest signal
        if positive_count > negative_count and positive_count > neutral_count:
            emotion = 'positive'
            confidence = min(0.85, (positive_count / max(total_signals, 1)) + 0.3)
        elif negative_count > positive_count and negative_count > neutral_count:
            emotion = 'negative'
            confidence = min(0.85, (negative_count / max(total_signals, 1)) + 0.3)
        else:
            emotion = 'neutral'
            confidence = 0.6 + (neutral_count / max(total_signals * 2, 1))
        
        return {
            'emotion': emotion,
            'confidence': min(confidence, 0.95),
            'positive_signals': positive_count,
            'negative_signals': negative_count,
            'neutral_signals': neutral_count,
            'method': 'keyword_fallback'
        }