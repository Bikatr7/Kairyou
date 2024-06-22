## Copyright 2024 Kaden Bilyeu (Bikatr7) (https://github.com/Bikatr7) (https://github.com/Bikatr7/Kairyou)
## Use of this source code is governed by a GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

from kairyou import Kairyou, Indexer
from kairyou import KatakanaUtil

##-------------------start-of-read_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
        
    except:
        raise FileNotFoundError("File not found")
    
##-------------------start-of-main()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():

    text = read_file("tests//testing_preprocessing_text.txt")
    testing_knowledge_base = read_file("tests//testing_knowledge_base.txt")

    names_and_occurrences, indexing_log = Indexer.index(text, testing_knowledge_base, "tests//testing_replacements.json")

    preprocessed_text, preprocessing_log, error_log = Kairyou.preprocess(text, "tests//testing_replacements.json")

    katakana_only = KatakanaUtil.is_katakana_only("テスト")

    not_katakana_only = KatakanaUtil.is_katakana_only("テストtest")

    punctuation_string = ".。。"

    length_of_katakana_words = len(KatakanaUtil.katakana_words)

    if(not katakana_only or not_katakana_only):
        raise ValueError("Test failed")
    
    if(length_of_katakana_words < 5000):
        raise ValueError("Test failed")
    
    if(not KatakanaUtil.is_punctuation(punctuation_string)):
        raise ValueError("Test failed")
    
    if(not KatakanaUtil.is_repeating_sequence("テストテスト")):
        raise ValueError("Test failed")
    
    if(KatakanaUtil.is_repeating_sequence("テスト")):
        raise ValueError("Test failed") 
    
    if(not KatakanaUtil.is_partially_english("テストtest")):
        raise ValueError("Test failed")
    
    if(KatakanaUtil.is_partially_english("テスト")):
        raise ValueError("Test failed")
    
    print("All tests passed")


if(__name__ == "__main__"):
    main()