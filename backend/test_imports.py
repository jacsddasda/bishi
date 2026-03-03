# Test script to check module imports
print("Testing module imports...")

# Test Flask import
try:
    from flask import Flask
    print("✓ Flask imported successfully")
except Exception as e:
    print(f"✗ Flask import failed: {e}")

# Test other imports
try:
    from app.services.pdf_parser import parse_pdf
    print("✓ pdf_parser imported successfully")
except Exception as e:
    print(f"✗ pdf_parser import failed: {e}")

try:
    from app.services.info_extractor import extract_info
    print("✓ info_extractor imported successfully")
except Exception as e:
    print(f"✗ info_extractor import failed: {e}")

try:
    from app.services.resume_scorer import score_resume
    print("✓ resume_scorer imported successfully")
except Exception as e:
    print(f"✗ resume_scorer import failed: {e}")

try:
    from app.utils.cache import get_cache, set_cache
    print("✓ cache imported successfully")
except Exception as e:
    print(f"✗ cache import failed: {e}")

print("Import test completed!")
