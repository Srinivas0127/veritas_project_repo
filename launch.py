#!/usr/bin/env python3
"""
Veritas Quick Start Script
Handles common startup issues and provides helpful guidance
"""

import subprocess
import sys
import time
import os
import signal
import atexit

class VeritasLauncher:
    def __init__(self):
        self.server_process = None
        
    def cleanup(self):
        """Clean up server process on exit"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=3)
            except:
                if self.server_process:
                    self.server_process.kill()
    
    def kill_existing_servers(self):
        """Kill any existing Flask/Python servers on common ports"""
        ports = [5000, 5001, 5002, 8000, 8080]
        for port in ports:
            try:
                result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                      capture_output=True, text=True, timeout=5)
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            print(f"🧹 Stopped existing process on port {port}")
                        except:
                            pass
            except:
                pass
    
    def start_server(self):
        """Start the Veritas server"""
        try:
            print("🛡️  Veritas News Credibility Analysis System")
            print("=" * 50)
            
            # Kill existing servers
            self.kill_existing_servers()
            time.sleep(1)
            
            # Change to the script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)
            
            print("🚀 Starting Veritas server...")
            
            # Start server as subprocess
            self.server_process = subprocess.Popen([
                sys.executable, 'start.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
               universal_newlines=True, bufsize=1)
            
            # Wait for startup messages
            startup_timeout = 15
            start_time = time.time()
            
            while time.time() - start_time < startup_timeout:
                if self.server_process.poll() is not None:
                    # Process ended
                    print("❌ Server failed to start")
                    return False
                    
                try:
                    line = self.server_process.stdout.readline()
                    if line:
                        print(line.strip())
                        if "Running on" in line:
                            print("\n✅ Server started successfully!")
                            print("📡 Open your browser to: http://localhost:5000")
                            print("🎯 Try analyzing a news article URL")
                            print("\n🛑 Press Ctrl+C to stop the server")
                            print("=" * 50)
                            return True
                except:
                    pass
                    
                time.sleep(0.1)
            
            print("⏰ Server taking longer than expected to start...")
            return True
            
        except KeyboardInterrupt:
            print("\n🛑 Startup cancelled by user")
            return False
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def run(self):
        """Main run method"""
        # Register cleanup function
        atexit.register(self.cleanup)
        
        if not self.start_server():
            return 1
            
        try:
            # Keep the launcher running
            while True:
                if self.server_process and self.server_process.poll() is not None:
                    print("❌ Server process ended unexpectedly")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping Veritas server...")
            self.cleanup()
            print("✅ Server stopped successfully")
        
        return 0

def main():
    launcher = VeritasLauncher()
    sys.exit(launcher.run())

if __name__ == "__main__":
    main()