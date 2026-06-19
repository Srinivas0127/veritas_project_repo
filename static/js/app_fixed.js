// Veritas News Analysis - Clean Frontend

class VeritasAnalyzer {
    constructor() {
        this.init();
        this.isAnalyzing = false;
    }

    init() {
        this.bindEvents();
        console.log('✅ Veritas Analyzer initialized');
    }

    bindEvents() {
        // Form submission
        const analyzeForm = document.getElementById('analyzeForm');
        analyzeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!this.isAnalyzing) {
                this.analyzeArticle();
            }
        });

        // URL input validation
        const urlInput = document.getElementById('urlInput');
        urlInput.addEventListener('input', () => {
            this.validateUrl();
        });
    }

    validateUrl() {
        const urlInput = document.getElementById('urlInput');
        const url = urlInput.value.trim();
        
        if (url && !this.isValidUrl(url)) {
            urlInput.setCustomValidity('Please enter a valid news article URL');
        } else {
            urlInput.setCustomValidity('');
        }
    }

    isValidUrl(string) {
        try {
            const url = new URL(string);
            return url.protocol === 'http:' || url.protocol === 'https:';
        } catch (_) {
            return false;
        }
    }

    async analyzeArticle() {
        const url = document.getElementById('urlInput').value.trim();
        
        console.log('🔍 Starting analysis for URL:', url);
        
        if (!url) {
            this.showError('Please enter a news article URL');
            return;
        }

        if (!this.isValidUrl(url)) {
            this.showError('Please enter a valid URL (must start with http:// or https://)');
            return;
        }

        this.isAnalyzing = true;
        this.showLoading();

        try {
            console.log('📡 Making API request to /api/analyze');
            
            // Make API request
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP ${response.status}: Analysis failed`);
            }

            const results = await response.json();
            console.log('📊 API Response received:', results);
            
            // Show results
            this.displayResults(results);

        } catch (error) {
            console.error('❌ Analysis failed:', error);
            this.showError(error.message || 'Analysis failed. Please try again.');
        } finally {
            this.isAnalyzing = false;
        }
    }

    showLoading() {
        this.hideAllSections();
        document.getElementById('loadingState').classList.remove('hidden');
        
        // Disable form
        const analyzeBtn = document.getElementById('analyzeBtn');
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    }

    showError(message) {
        this.hideAllSections();
        document.getElementById('errorState').classList.remove('hidden');
        document.getElementById('errorMessage').textContent = message;
        this.resetForm();
    }

    displayResults(results) {
        console.log('🎉 Displaying results:', results);
        
        this.hideAllSections();
        document.getElementById('resultsSection').classList.remove('hidden');
        this.resetForm();
        
        // Populate article information
        this.displayArticleInfo(results.article);
        
        // Display analysis results
        this.displayCredibilityScore(results.analysis.credibility);
        this.displaySentimentAnalysis(results.analysis.emotion);
        this.displaySummary(results.analysis.summary);
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    displayArticleInfo(article) {
        console.log('📰 Displaying article info:', article);
        document.getElementById('articleTitle').textContent = article.title || 'Untitled Article';
        document.getElementById('articleSource').textContent = this.formatSourceName(article.source_domain);
        
        const urlLink = document.getElementById('articleUrl');
        urlLink.href = article.url;
        urlLink.style.display = 'flex';
    }

    displayCredibilityScore(credibility) {
        const score = Math.round(credibility.final_score);
        const scoreElement = document.getElementById('credibilityScore');
        const levelElement = document.getElementById('credibilityLevel');
        const descriptionElement = document.getElementById('credibilityDescription');
        
        console.log('🎯 Displaying credibility score:', score);
        
        // Update score with animation
        this.animateCounter(scoreElement, score);
        
        // Update visual elements
        const interpretation = credibility.interpretation;
        if (levelElement) levelElement.textContent = interpretation.level;
        if (descriptionElement) descriptionElement.textContent = interpretation.description;
        
        // Update score circle color based on score
        const scoreCircle = scoreElement.closest('.score-circle');
        if (scoreCircle) {
            this.updateScoreColor(scoreCircle, score);
        }
    }

    displaySentimentAnalysis(emotion) {
        const iconElement = document.getElementById('sentimentIcon');
        const labelElement = document.getElementById('sentimentLabel');
        const confidenceElement = document.getElementById('sentimentConfidence');
        
        console.log('💝 Displaying sentiment:', emotion);
        
        // Update sentiment display
        const sentiment = emotion.emotion || 'neutral';
        
        if (iconElement) {
            iconElement.className = `sentiment-icon ${sentiment}`;
            
            // Set appropriate icon
            const icons = {
                positive: 'fas fa-smile',
                negative: 'fas fa-frown',
                neutral: 'fas fa-meh'
            };
            iconElement.innerHTML = `<i class="${icons[sentiment] || icons.neutral}"></i>`;
        }
        
        if (labelElement) labelElement.textContent = this.capitalizeFirst(sentiment);
        if (confidenceElement) confidenceElement.textContent = Math.round((emotion.confidence || 0) * 100);
    }

    displaySummary(summary) {
        const summaryElement = document.getElementById('articleSummary');
        
        console.log('📄 Displaying summary:', summary);
        
        if (summaryElement) {
            if (summary && summary.length > 0) {
                summaryElement.textContent = summary;
                summaryElement.style.fontStyle = 'normal';
                summaryElement.style.opacity = '1';
            } else {
                summaryElement.textContent = 'Summary not available for this article.';
                summaryElement.style.fontStyle = 'italic';
                summaryElement.style.opacity = '0.7';
            }
        }
    }

    // Utility methods
    animateCounter(element, target) {
        const duration = 1500;
        const startTime = Date.now();
        const startValue = 0;
        
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = this.easeOutQuart(progress);
            const current = Math.round(startValue + (target - startValue) * easeProgress);
            
            element.textContent = current;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }

    easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    updateScoreColor(scoreCircle, score) {
        // Update border color based on score
        if (score >= 80) {
            scoreCircle.style.borderColor = '#10b981'; // success
            scoreCircle.style.color = '#10b981';
        } else if (score >= 65) {
            scoreCircle.style.borderColor = '#84cc16'; // good
            scoreCircle.style.color = '#84cc16';
        } else if (score >= 50) {
            scoreCircle.style.borderColor = '#f59e0b'; // warning
            scoreCircle.style.color = '#f59e0b';
        } else if (score >= 35) {
            scoreCircle.style.borderColor = '#f97316'; // orange
            scoreCircle.style.color = '#f97316';
        } else {
            scoreCircle.style.borderColor = '#ef4444'; // danger
            scoreCircle.style.color = '#ef4444';
        }
    }

    formatSourceName(domain) {
        if (!domain) return 'Unknown Source';
        
        // Remove www. and common suffixes
        let name = domain.replace(/^www\./, '').replace(/\.(com|org|net|co\.uk)$/, '');
        
        // Capitalize and format common sources
        const sourceMap = {
            'bbc': 'BBC',
            'cnn': 'CNN',
            'reuters': 'Reuters',
            'nytimes': 'New York Times',
            'washingtonpost': 'Washington Post',
            'theguardian': 'The Guardian',
            'foxnews': 'Fox News',
            'npr': 'NPR',
            'wsj': 'Wall Street Journal'
        };
        
        return sourceMap[name.toLowerCase()] || this.capitalizeFirst(name);
    }

    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    hideAllSections() {
        ['loadingState', 'errorState', 'resultsSection'].forEach(id => {
            document.getElementById(id).classList.add('hidden');
        });
    }

    resetForm() {
        const analyzeBtn = document.getElementById('analyzeBtn');
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze';
    }
}

// Global functions for UI interactions
function clearResults() {
    const analyzer = window.veritas;
    analyzer.hideAllSections();
    
    // Clear and focus input
    const urlInput = document.getElementById('urlInput');
    urlInput.value = '';
    urlInput.focus();
    
    // Reset form
    analyzer.resetForm();
}

function shareResults() {
    try {
        const title = document.getElementById('articleTitle').textContent;
        const score = document.getElementById('credibilityScore').textContent;
        const level = document.getElementById('credibilityLevel').textContent;
        const url = document.getElementById('articleUrl').href;
        
        const shareText = `📊 Credibility Analysis: "${title}" scored ${score}/100 (${level}) via Veritas News Analysis. ${url}`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Veritas News Analysis',
                text: shareText,
                url: window.location.href
            });
        } else {
            // Fallback to clipboard
            navigator.clipboard.writeText(shareText).then(() => {
                // Show temporary success message
                const btn = event.target.closest('button');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                btn.style.background = '#10b981';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.background = '';
                }, 2000);
            }).catch(() => {
                alert('Unable to copy to clipboard');
            });
        }
    } catch (error) {
        console.error('Share failed:', error);
        alert('Unable to share results');
    }
}

// Initialize the analyzer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.veritas = new VeritasAnalyzer();
});