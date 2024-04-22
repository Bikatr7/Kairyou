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


if(__name__ == "__main__"):
    main()