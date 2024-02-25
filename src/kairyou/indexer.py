## built-in libraries
import os
import typing
import json
import time

## third-party libraries
import spacy

## custom modules
from .util import validate_replacement_json, get_elapsed_time
from .katakana_util import KatakanaUtil
from .types import NameAndOccurrence

class Indexer:

    """

    The global Indexer client for indexing names.

    """

    replacement_json:dict

    json_type:typing.Literal["kudasai", "fukuin"]

    text_to_index:str

    indexing_log = ""

    knowledge_base:typing.List[str] = []

    blacklisted_names:typing.List[str] = []

    ## dict of entity labels and their occurrences
    entity_occurrences:dict = {}

    ner = spacy.load("ja_core_news_lg")

##-------------------start-of-load_static_data()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def load_static_data(text_to_index:str, knowledge_base:str, replacement_json:typing.Union[str, dict]) -> None:
        
        """
        
        Loads static data into the Indexer class.

        """

        ## text_to_index can be sent in a path to a text file, or just the text itself
        if(os.path.exists(text_to_index)):
            with open(text_to_index, "r", encoding="utf-8") as file:
                Indexer.text_to_index = file.read()

        else:
            Indexer.text_to_index = text_to_index

        ## knowledge_base can be sent in a path to a directory containing text files, a path to a text file, or just the text itself            
        if(os.path.exists(knowledge_base)):
            if(os.path.isdir(knowledge_base)):
                for file in os.listdir(knowledge_base):
                    if(file.endswith(".txt")):
                      with open(os.path.join(knowledge_base, file), "r", encoding="utf-8") as file:
                          Indexer.knowledge_base.append(file.read())
            else:
                with open(knowledge_base, "r", encoding="utf-8") as file:
                    Indexer.knowledge_base.append(file.read())

        else:
            Indexer.knowledge_base.append(knowledge_base)

        ## replacement_json can be sent in a path to a json, or as the json itself
        if(isinstance(replacement_json, str)):

            with open(replacement_json, "r", encoding="utf-8") as file:

                Indexer.replacement_json = json.load(file)

        else:

            Indexer.replacement_json = replacement_json
                        
##-------------------start-of-get_names_from_replacement_json()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_names_from_replacement_json():

        """
        
        Fetches all names from the replacement_json and returns them as a list.

        """

        entries = []

        Indexer.json_type, _ = validate_replacement_json(Indexer.replacement_json)

        if(Indexer.json_type == "kudasai"):

            key_to_fetch_from = ["single_names", "full_names"]

        else:
            
            key_to_fetch_from = ["names", "single-names", "full-names"]

        for key in key_to_fetch_from:

            ## entries can sometimes look like ("Yamanaka Ikuko": ["山中","郁子"])
            ## so we need to split the japanese names and add them to the list

            entry = Indexer.replacement_json.get(key, [])

            if(isinstance(entry, tuple) or isinstance(entry, list)):

                for name in entry:

                    entries.append(name)

            elif(isinstance(entry, dict)):
                
                for name in entry.values():

                    entries.extend(name if isinstance(name, list) else [name])

            else:

                entries.append(entry)

        return list(set(entries))        

##-------------------start-of-get_names_from_all_sources()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_names_from_all_sources() -> typing.Tuple[typing.List[NameAndOccurrence], typing.List[NameAndOccurrence], typing.List[NameAndOccurrence]]:
        
        """
        
        Fetches all names from the knowledge_base, text_to_index, and replacement_json and returns them as a list.

        """

        names_in_knowledge_base = []
        names_in_text_to_index = []
        names_in_replacement_json = [NameAndOccurrence(name, 1) for name in Indexer.get_names_from_replacement_json()]

        name_occurrences = {}
        for entry in Indexer.knowledge_base:
            entry = entry.split("\n")
            for line in entry:
                sentence = Indexer.ner(line)
                for entity in sentence.ents:

                    if(entity.text in Indexer.blacklisted_names):
                        continue

                    ## log label and occurrence
                    Indexer.entity_occurrences[entity.label_] = Indexer.entity_occurrences.get(entity.label_, 0) + 1

                    if(entity.label_ == "PERSON"):
                        name_occurrences[entity.text] = name_occurrences.get(entity.text, 0) + 1
                        names_in_knowledge_base.append(NameAndOccurrence(entity.text, name_occurrences[entity.text]))

        name_occurrences = {}
        for entry in Indexer.text_to_index.split("\n"):
            sentence = Indexer.ner(entry)
            for entity in sentence.ents:

                if(entity.text in Indexer.blacklisted_names):
                    continue

                ## log label and occurrence
                Indexer.entity_occurrences[entity.label_] = Indexer.entity_occurrences.get(entity.label_, 0) + 1

                if(entity.label_ == "PERSON"):
                    name_occurrences[entity.text] = name_occurrences.get(entity.text, 0) + 1
                    names_in_text_to_index.append(NameAndOccurrence(entity.text, name_occurrences[entity.text]))

        return names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json
    
##-------------------start-of-perform_further_elimination()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def perform_further_elimination(names_in_knowledge_base:typing.List[NameAndOccurrence], 
                                    names_in_text_to_index:typing.List[NameAndOccurrence], 
                                    names_in_replacement_json:typing.List[NameAndOccurrence]) -> typing.Tuple[typing.List[NameAndOccurrence], typing.List[NameAndOccurrence], typing.List[NameAndOccurrence]]:
        
        """
        
        Performs further elimination of names.

        Elimination Criteria:
        1. "Names" that consist of more punctuation than letters.
        2. "Names" that are actual katakana words. See words.py
        3. "Names" that are partialy english. (Contains at least one english letter)
        4. "Names" that appear to be onomatopoeia. (Repeating character sequences)

        """

        names_in_knowledge_base = [name for name in names_in_knowledge_base if not (KatakanaUtil.is_more_punctuation_than_japanese(name.name) or 
                                                                                    KatakanaUtil.is_actual_word(name.name) or 
                                                                                    KatakanaUtil.is_partialy_english(name.name) or
                                                                                    KatakanaUtil.is_repeating_sequence(name.name))]
        
        names_in_text_to_index = [name for name in names_in_text_to_index if not (KatakanaUtil.is_more_punctuation_than_japanese(name.name) or 
                                                                                  KatakanaUtil.is_actual_word(name.name) or 
                                                                                    KatakanaUtil.is_partialy_english(name.name) or
                                                                                  KatakanaUtil.is_repeating_sequence(name.name))]
        
        names_in_replacement_json = [name for name in names_in_replacement_json if not (KatakanaUtil.is_more_punctuation_than_japanese(name.name) or 
                                                                                        KatakanaUtil.is_actual_word(name.name) or 
                                                                                        KatakanaUtil.is_partialy_english(name.name) or
                                                                                        KatakanaUtil.is_repeating_sequence(name.name))]


        return names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json
    
##-------------------start-of-trim_honorifics()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def trim_honorifics(names_in_knowledge_base:typing.List[NameAndOccurrence], 
                        names_in_text_to_index:typing.List[NameAndOccurrence], 
                        names_in_replacement_json:typing.List[NameAndOccurrence]) -> typing.Tuple[typing.List[NameAndOccurrence], typing.List[NameAndOccurrence], typing.List[NameAndOccurrence]]:
        
        """
        
        Trims honorifics from names.

        """

        honorifics = Indexer.replacement_json.get('honorifics', [])

        for honorific in honorifics:
            names_in_knowledge_base = [NameAndOccurrence(name.name.replace(honorific, ""), name.occurrence) for name in names_in_knowledge_base]
            names_in_text_to_index = [NameAndOccurrence(name.name.replace(honorific, ""), name.occurrence) for name in names_in_text_to_index]
            names_in_replacement_json = [NameAndOccurrence(name.name.replace(honorific, ""), name.occurrence) for name in names_in_replacement_json]

        return names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json
    
##-------------------start-of-is_name_in_other_sources()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_name_in_other_sources(name: str, all_names: typing.Set[str]) -> bool:

        """

        Checks if a name is in the knowledge_base or replacement_json.

        """


        return any(other_name in name for other_name in all_names)
    
##-------------------start-of-index()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def index(text_to_index:str, 
              knowledge_base:str, 
              replacement_json:typing.Union[str, dict],
              blacklist:typing.List[str] = []
              ) -> typing.Tuple[typing.List[NameAndOccurrence], str]:

        """
        
        Determines which names in the text_to_index are not in the knowledge_base or replacement_json and returns them as a list.

        Returns a tuple of tuples. That tuple has the name itself and the occurrence of the name that was flagged.

        Parameters:
        text_to_index (str): The text to index. Can be a path to a text file, or just the text itself.
        knowledge_base (str): The knowledge base. Can be a path to a directory containing text files, a path to a text file, or just the text itself.
        replacement_json (str): The replacement json. Can be a path to a json, or as the json itself.
        blacklist (list): A list of strings to ignore.

        Returns:
        new_names (NameAndOccurrence): A list of names that are not in the knowledge_base or replacement_json. (NameAndOccurrence is a named tuple with the fields name and occurrence).
        Indexer.indexing_log (str): Log of the indexing process (names that were flagged as unique 'names' and which occurrence they were flagged at).
        
        """

        time_start = time.time()

        if(len(blacklist) > 0):
            Indexer.blacklisted_names = blacklist

        new_names:typing.List[NameAndOccurrence] = []

        Indexer.load_static_data(text_to_index, knowledge_base, replacement_json)

        names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json = Indexer.get_names_from_all_sources()

        names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json = Indexer.perform_further_elimination(names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json)

        if(replacement_json):
            names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json = Indexer.trim_honorifics(names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json)

        names_in_knowledge_base = set(name.name for name in names_in_knowledge_base)
        names_in_replacement_json = set(name.name for name in names_in_replacement_json)

        all_names = names_in_knowledge_base | names_in_replacement_json

        for name in names_in_text_to_index:
            if(not Indexer.is_name_in_other_sources(name.name, all_names)):
                new_names.append(name)
                Indexer.indexing_log += (f"Name: {name.name} Occurrence: {name.occurrence} was flagged as a unique 'name'\n")

        time_end = time.time()

        Indexer.indexing_log += "\nIgnored Strings: " + str(Indexer.blacklisted_names)

        Indexer.indexing_log += "\nTotal Unique 'Names'  : " + \
            str(len(new_names))
        Indexer.indexing_log += "\nTime Elapsed : " + \
            get_elapsed_time(time_start, time_end)

        return new_names, Indexer.indexing_log