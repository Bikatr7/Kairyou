#!/usr/bin/env python3

"""
Simple test script for the new postprocess functionality.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from kairyou import Kairyou

def test_postprocess():
    """Test the postprocess functionality"""
    
    text = "The students at Advanced Nurturing High School respect their senpai and help their kōhai."
    
    replacement_json = {
        "honorifics": {},
        "single_words": {},
        "unicode": {},
        "phrases": {},
        "kutouten": {},
        "name_like": {},
        "single_names": {},
        "full_names": {},
        "enhanced_check_whitelist": {},
        "postprocess": {
            "Advanced Nurturing High School": "ANHS",
            "senpai": "senior",
            "kōhai": "junior"
        }
    }
    
    print("Original text:")
    print(text)
    print()
    
    try:
        preprocessed_text, log, error_log = Kairyou.preprocess(text, replacement_json)
        
        print("Processed text:")
        print(preprocessed_text)
        print()
        
        print("Processing log:")
        print(log)
        print()
        
        if(error_log):
            print("Error log:")
            print(error_log)
        else:
            print("No errors!")
            
        expected_text = "The students at ANHS respect their senior and help their junior."
        if(preprocessed_text == expected_text):
            print("\n✅ Test PASSED! Postprocess functionality works correctly.")
        else:
            print(f"\n❌ Test FAILED! Expected: '{expected_text}', Got: '{preprocessed_text}'") 
            
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()

if(__name__ == "__main__"):
    test_postprocess() 