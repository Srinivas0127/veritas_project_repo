#!/bin/bash
# Veritas Setup Script
# Automated setup for the Veritas News Analysis System

echo "🛡️  Setting up Veritas News Credibility Analysis System..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "📖 Downloading NLTK data..."
python3 -c "
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
print('✅ NLTK data downloaded')
"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p models
mkdir -p logs
mkdir -p static/uploads

# Set permissions
chmod +x app.py

# Verify installation
echo "🧪 Verifying installation..."
python3 -c "
import sys
import importlib

required_packages = [
    'flask', 'transformers', 'torch', 'newspaper', 'beautifulsoup4', 
    'requests', 'numpy', 'nltk'
]

missing_packages = []
for package in required_packages:
    try:
        importlib.import_module(package)
        print(f'✅ {package}')
    except ImportError:
        missing_packages.append(package)
        print(f'❌ {package}')

if missing_packages:
    print(f'\\n🚨 Missing packages: {missing_packages}')
    print('Please run: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('\\n🎉 All packages installed successfully!')
"

# Create run script
echo "📝 Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
# Veritas Run Script

echo "🛡️  Starting Veritas News Analysis System..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Start the application
echo "🚀 Starting Flask application..."
echo "📡 Server will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo ""

python app.py
EOF

chmod +x run.sh

# Create environment file template
echo "⚙️  Creating environment template..."
cat > .env.example << 'EOF'
# Veritas Environment Configuration
# Copy this file to .env and customize as needed

# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
HOST=0.0.0.0
PORT=5000

# AI Model Configuration
AI_MODEL_CACHE_DIR=./models
MAX_CONTENT_LENGTH=10000

# Web Scraping Configuration
SCRAPING_TIMEOUT=30
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

# Rate Limiting
RATELIMIT_ENABLED=False
REQUESTS_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
EOF

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Quick Start:"
echo "1. Run the application: ./run.sh"
echo "2. Open browser to: http://localhost:5000"
echo "3. Enter a news article URL to analyze"
echo ""
echo "📚 Additional Commands:"
echo "• Test installation: python -c 'from modules import *; print(\"✅ All modules loaded\")'"
echo "• Run health check: curl http://localhost:5000/api/health"
echo "• View logs: tail -f logs/veritas.log"
echo ""
echo "⚠️  Note: First AI model load may take 1-2 minutes"
echo "💡 For production deployment, copy .env.example to .env and customize"