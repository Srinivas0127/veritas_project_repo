#!/usr/bin/env python3
"""
Simple Veritas Launcher - Direct Flask App Runner
"""

import sys
import os

def main():
    print("🛡️  Starting Veritas (Simple Mode)")
    
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from app import app
        
        # Try multiple ports
        for port in [8080, 8000, 5001, 5002, 3000]:
            try:
                print(f"🔌 Attempting to start on port {port}...")
                print(f"📡 Open browser to: http://localhost:{port}")
                print("🛑 Press Ctrl+C to stop\n")
                
                app.run(
                    host='127.0.0.1',
                    port=port,
                    debug=True,
                    use_reloader=False
                )
                break
                
            except OSError as e:
                if "Address already in use" in str(e):
                    print(f"   Port {port} busy, trying next...")
                    continue
                else:
                    print(f"   Error: {e}")
                    continue
        else:
            print("❌ No available ports found")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()