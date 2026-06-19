"""
AI Analyzer Module for Veritas News Analysis
Handles text summarization using BART and emotion detection using RoBERTa
"""

import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import re
import torch

logger = logging.getLogger(__name__)

class AIAnalyzer:
    def __init__(self):
        self.summarizer = None
        self.emotion_analyzer = None
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Initialize models lazily for better startup time
        self._init_models()
    
    def _init_models(self):
        """Initialize AI models with error handling and fallbacks"""
        try:
            logger.info("Initializing BART summarization model...")
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=self.device
            )
            logger.info("BART model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load BART model: {str(e)}")
            self.summarizer = None
        
        try:
            logger.info("Initializing RoBERTa emotion detection model...")
            self.emotion_analyzer = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-roberta-base-emotion",
                device=self.device
            )
            logger.info("RoBERTa emotion model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load RoBERTa model: {str(e)}")
            self.emotion_analyzer = None
    
    def summarize_text(self, text, max_length=150, min_length=30):
        """
        Generate summary using BART model
        Falls back to extractive summarization if BART fails
        """
        if not text or len(text.strip()) < 50:
            return "Text too short to summarize"
        
        # Try AI summarization first
        if self.summarizer:
            try:
                # Clean and prepare text
                clean_text = self._clean_text_for_ai(text)
                
                # BART has token limits, so chunk if needed
                if len(clean_text) > 1000:
                    clean_text = clean_text[:1000]
                
                summary_result = self.summarizer(
                    clean_text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                
                summary = summary_result[0]['summary_text']
                logger.info("Successfully generated AI summary")
                return summary
                
            except Exception as e:
                logger.error(f"BART summarization failed: {str(e)}")
        
        # Fallback to extractive summarization
        logger.info("Using fallback extractive summarization")
        return self._extractive_summary(text, max_sentences=3)
    
    def detect_emotion(self, text):
        """
        Detect emotion using RoBERTa model
        Falls back to keyword-based emotion detection if RoBERTa fails
        """
        if not text or len(text.strip()) < 10:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'method': 'insufficient_text'
            }
        
        # Try AI emotion detection first
        if self.emotion_analyzer:
            try:
                # Clean and prepare text
                clean_text = self._clean_text_for_ai(text)
                
                # Limit text length for emotion analysis
                if len(clean_text) > 500:
                    clean_text = clean_text[:500]
                
                emotion_result = self.emotion_analyzer(clean_text)
                
                # Map detailed emotions to simplified categories
                emotion_mapping = {
                    'joy': 'positive',
                    'optimism': 'positive',
                    'love': 'positive',
                    'sadness': 'negative',
                    'anger': 'negative',
                    'fear': 'negative',
                    'pessimism': 'negative',
                    'disgust': 'negative',
                    'surprise': 'neutral',
                    'trust': 'positive',
                    'anticipation': 'neutral'
                }
                
                raw_emotion = emotion_result[0]['label'].lower()
                confidence = emotion_result[0]['score']
                
                simplified_emotion = emotion_mapping.get(raw_emotion, 'neutral')
                
                logger.info(f"AI emotion detection: {simplified_emotion} (confidence: {confidence:.2f})")
                
                return {
                    'emotion': simplified_emotion,
                    'confidence': confidence,
                    'raw_emotion': raw_emotion,
                    'method': 'roberta_ai'
                }
                
            except Exception as e:
                logger.error(f"RoBERTa emotion detection failed: {str(e)}")
        
        # Fallback to keyword-based emotion detection
        logger.info("Using fallback keyword-based emotion detection")
        return self._keyword_emotion_detection(text)
    
    def _clean_text_for_ai(self, text):
        """Clean text for AI model processing"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        return text.strip()
    
    def _extractive_summary(self, text, max_sentences=3):
        """Fallback extractive summarization using first few meaningful sentences"""
        try:
            sentences = self._split_sentences(text)
            
            # Filter out very short sentences and likely navigation text
            meaningful_sentences = []
            for sentence in sentences:
                if (len(sentence) > 20 and 
                    not any(skip_word in sentence.lower() for skip_word in 
                           ['click here', 'read more', 'subscribe', 'sign up', 'follow us'])):
                    meaningful_sentences.append(sentence.strip())
            
            # Take first few meaningful sentences
            summary_sentences = meaningful_sentences[:max_sentences]
            
            if summary_sentences:
                return ' '.join(summary_sentences)
            else:
                return "Unable to generate meaningful summary"
                
        except Exception as e:
            logger.error(f"Extractive summarization failed: {str(e)}")
            return "Summary generation failed"
    
    def _split_sentences(self, text):
        """Simple sentence splitting"""
        # Split on sentence endings
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _keyword_emotion_detection(self, text):
        """Fallback emotion detection using keyword analysis"""
        text_lower = text.lower()
        
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
            'positive', 'success', 'achievement', 'victory', 'win', 'progress',
            'improve', 'benefit', 'advantage', 'opportunity', 'hope', 'optimistic'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'fail', 'failure',
            'crisis', 'disaster', 'tragedy', 'problem', 'issue', 'concern',
            'worry', 'fear', 'angry', 'sad', 'disappointed', 'frustrated',
            'devastating', 'shocking', 'outrageous'
        ]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count and positive_count > 0:
            emotion = 'positive'
            confidence = min(0.8, positive_count / 10)
        elif negative_count > positive_count and negative_count > 0:
            emotion = 'negative'
            confidence = min(0.8, negative_count / 10)
        else:
            emotion = 'neutral'
            confidence = 0.5
        
        return {
            'emotion': emotion,
            'confidence': confidence,
            'positive_signals': positive_count,
            'negative_signals': negative_count,
            'method': 'keyword_fallback'
        }