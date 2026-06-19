#!/usr/bin/env python3
"""
Veritas News Analysis System - Production Launcher
Run this script to start the Veritas application
"""

import os
import sys
import logging
from datetime import datetime

def setup_logging():
    """Configure logging for the application"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"veritas-{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = [
        'flask', 'newspaper', 'beautifulsoup4', 'requests'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            if module == 'beautifulsoup4':
                try:
                    import bs4
                except ImportError:
                    missing_modules.append(module)
            elif module == 'newspaper':
                try:
                    import newspaper
                except ImportError:
                    missing_modules.append('newspaper3k')
            else:
                missing_modules.append(module)
    
    if missing_modules:
        print("❌ Missing required dependencies:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n💡 Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are available")
    return True

def main():
    """Main entry point for the Veritas application"""
    print("🛡️  Veritas News Credibility Analysis System")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        from app import app
        
        print("\n🚀 Starting Veritas server...")
        print(f" Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Try different ports if 5000 is in use
        ports_to_try = [8080, 8000, 5001, 5002, 3000]
        
        for port in ports_to_try:
            try:
                print(f"🔌 Trying to start server on port {port}...")
                print(f"📡 Server will be available at: http://localhost:{port}")
                app.run(
                    host='0.0.0.0',
                    port=port,
                    debug=False,  # Set to True for development
                    threaded=True
                )
                break
            except OSError as e:
                if "Address already in use" in str(e):
                    print(f"   Port {port} is busy, trying next port...")
                    continue
                else:
                    raise e
        else:
            print("❌ Could not find an available port. Please try manually:")
            print("   python app.py")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        logger.info("Server stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()