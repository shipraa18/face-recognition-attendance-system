#!/usr/bin/env python3
"""
Test script to verify deployment dependencies
"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        import flask
        print(f"✓ Flask {flask.__version__} imported successfully")
        
        import cv2
        print(f"✓ OpenCV {cv2.__version__} imported successfully")
        
        if hasattr(cv2, 'face'):
            print("✓ OpenCV face module available")
        else:
            print("⚠ OpenCV face module NOT available")
        
        import numpy as np
        print(f"✓ NumPy {np.__version__} imported successfully")
        
        import PIL
        print(f"✓ Pillow {PIL.__version__} imported successfully")
        
        print("\n✅ All basic imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
