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

    text_to_preprocess = read_file("tests//testing_preprocessing_text.txt")

    Kairyou.preprocess(text_to_preprocess, "tests//testing_replacements.json")


if(__name__ == "__main__"):
    main()