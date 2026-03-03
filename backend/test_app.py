# Test script to check Flask app startup
import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

print("Testing Flask app startup...")

try:
    from flask import Flask
    print("✓ Flask imported successfully")
    
    # Create a simple app
    app = Flask(__name__)
    print("✓ Flask app created successfully")
    
    @app.route('/test')
    def test():
        return "Test success"
    
    print("✓ Route added successfully")
    
    # Try to get the app context
    with app.app_context():
        print("✓ App context created successfully")
        
    print("All tests passed! Flask app is working correctly.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
