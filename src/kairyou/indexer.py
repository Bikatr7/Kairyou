## Copyright 2024 Kaden Bilyeu (Bikatr7) (https://github.com/Bikatr7) (https://github.com/Bikatr7/Kairyou)
## Use of this source code is governed by a GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import os
import typing
import json
import time

## third-party libraries
import spacy

## custom modules
from .util import _validate_replacement_json, _get_elapsed_time
from .katakana_util import KatakanaUtil
from .types import NameAndOccurrence
from .exceptions import InvalidReplacementJsonPath, SpacyModelNotFound

class Indexer:

    """

    The global Indexer client for indexing names.

    """

    _replacement_json:dict

    _json_type:typing.Literal["kudasai", "fukuin"]

    _text_to_index:str

    indexing_log = ""

    _knowledge_base:typing.List[str] = []

    _blacklisted_names:typing.List[str] = []

    ## dict of entity labels and their occurrences
    _entity_occurrences:dict = {}

    _ner:spacy.language.Language | None = None

##-------------------start-of-load_static_data()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def _load_static_data(text_to_index:str, knowledge_base:str, replacement_json:typing.Union[str, dict]) -> None:
        
        """
        
        Loads static data into the Indexer class.

        Parameters:
        text_to_index (str) : The text to index. Can be a path to a text file, or just the text itself.
        knowledge_base (str) : The knowledge base. Can be a path to a directory containing text files, a path to a text file, or just the text itself.
        replacement_json (str) : The replacement json. Can be a path to a json, or as the json itself.

        """

        ## text_to_index can be sent in a path to a text file, or just the text itself
        if(os.path.exists(text_to_index)):
            with open(text_to_index, "r", encoding="utf-8") as file:
                Indexer._text_to_index = file.read()

        else:
            Indexer._text_to_index = text_to_index

        ## knowledge_base can be sent in a path to a directory containing text files, a path to a text file, or just the text itself            
        if(os.path.exists(knowledge_base)):
            if(os.path.isdir(knowledge_base)):
                for file in os.listdir(knowledge_base):
                    if(file.endswith(".txt")):
                      with open(os.path.join(knowledge_base, file), "r", encoding="utf-8") as file:
                          Indexer._knowledge_base.append(file.read())
            else:
                with open(knowledge_base, "r", encoding="utf-8") as file:
                    Indexer._knowledge_base.append(file.read())

        else:
            Indexer._knowledge_base.append(knowledge_base)

        ## replacement_json can be sent in a path to a json, or as the json itself
        if(isinstance(replacement_json, str)):

            try:
                ## Try to load the string as JSON
                Indexer._replacement_json = json.loads(replacement_json)

            except json.JSONDecodeError:
                ## If it fails, treat the string as a file path
                if(os.path.isfile(replacement_json)):
                    with open(replacement_json, "r", encoding="utf-8") as file:
                        Indexer._replacement_json = json.load(file)
                else:
                    raise InvalidReplacementJsonPath(replacement_json)
        else:
            Indexer._replacement_json = replacement_json
                        
##-------------------start-of-_get_names_from_replacement_json()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _get_names_from_replacement_json() -> typing.List[str]:

        """
        
        Fetches all names from the replacement json and returns them as a list.

        Returns:
        list (str) : A list of names from the replacement json.

        """

        _entries = []

        Indexer._json_type, _ = _validate_replacement_json(Indexer._replacement_json)

        if(Indexer._json_type == "kudasai"):

            _key_to_fetch_from = ["single_names", "full_names"]

        else:
            
            _key_to_fetch_from = ["names", "single-names", "full-names"]

        for _key in _key_to_fetch_from:

            ## entries can sometimes look like ("Yamanaka Ikuko": ["山中","郁子"])
            ## so we need to split the japanese names and add them to the list

            _entry = Indexer._replacement_json.get(_key, [])

            if(isinstance(_entry, tuple) or isinstance(_entry, list)):

                for _name in _entry:

                    _entries.append(_name)

            elif(isinstance(_entry, dict)):
                
                for _name in _entry.values():

                    _entries.extend(_name if isinstance(_name, list) else [_name])

            else:

                _entries.append(_entry)

        return list(set(_entries))        

##-------------------start-of-_get_names_from_all_sources()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _get_names_from_all_sources() -> typing.Tuple[typing.List[NameAndOccurrence], typing.List[NameAndOccurrence], typing.List[NameAndOccurrence]]:
        
        """
        
        Fetches all names from the knowledge base, text to index, and replacement json and returns them as a list.

        Returns:
        names_in_knowledge_base (NameAndOccurrence): A list of names from the knowledge base.
        names_in_text_to_index (NameAndOccurrence): A list of names from the text to index.
        names_in_replacement_json (NameAndOccurrence): A list of names from the replacement json.

        """

        _names_in_knowledge_base = []
        _names_in_text_to_index = []
        _names_in_replacement_json = [NameAndOccurrence(_name, 1) for _name in Indexer._get_names_from_replacement_json()]

        _name_occurrences = {}
        for _entry in Indexer._knowledge_base:
            _entry = _entry.split("\n")
            for _line in _entry:
                assert Indexer._ner is not None, "Indexer._ner is None. Please ensure that the NER object is loaded before calling this method."
                _sentence = Indexer._ner(_line)
                for _entity in _sentence.ents:

                    if(_entity.text in Indexer._blacklisted_names):
                        continue

                    ## log label and occurrence
                    Indexer._entity_occurrences[_entity.label_] = Indexer._entity_occurrences.get(_entity.label_, 0) + 1

                    if(_entity.label_ == "PERSON"):
                        _name_occurrences[_entity.text] = _name_occurrences.get(_entity.text, 0) + 1
                        _names_in_knowledge_base.append(NameAndOccurrence(_entity.text, _name_occurrences[_entity.text]))

        _name_occurrences = {}
        for _entry in Indexer._text_to_index.split("\n"):
            assert Indexer._ner is not None, "Indexer._ner is None. Please ensure that the NER object is loaded before calling this method."
            _sentence = Indexer._ner(_entry)
            for _entity in _sentence.ents:

                if(_entity.text in Indexer._blacklisted_names):
                    continue

                ## log label and occurrence
                Indexer._entity_occurrences[_entity.label_] = Indexer._entity_occurrences.get(_entity.label_, 0) + 1

                if(_entity.label_ == "PERSON"):
                    _name_occurrences[_entity.text] = _name_occurrences.get(_entity.text, 0) + 1
                    _names_in_text_to_index.append(NameAndOccurrence(_entity.text, _name_occurrences[_entity.text]))

        return _names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json
    
##-------------------start-of-_perform_further_elimination()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def _perform_further_elimination(names_in_knowledge_base:typing.List[NameAndOccurrence], 
                                    names_in_text_to_index:typing.List[NameAndOccurrence], 
                                    names_in_replacement_json:typing.List[NameAndOccurrence]) -> typing.Tuple[typing.List[NameAndOccurrence], typing.List[NameAndOccurrence], typing.List[NameAndOccurrence]]:
        
        """
        
        Performs further elimination of names.

        Elimination Criteria:
        1. "Names" that consist of more punctuation than letters.
        2. "Names" that are actual katakana words. See words.py
        3. "Names" that are partialy english. (Contains at least one english letter)
        4. "Names" that appear to be onomatopoeia. (Repeating character sequences)

        Parameters:
        names_in_knowledge_base (NameAndOccurrence): A list of names from the knowledge base.
        names_in_text_to_index (NameAndOccurrence): A list of names from the text to index.
        names_in_replacement_json (NameAndOccurrence): A list of names from the replacement json.

        Returns:
        names_in_knowledge_base (NameAndOccurrence): A list of names from the knowledge base.
        names_in_text_to_index (NameAndOccurrence): A list of names from the text to index.
        names_in_replacement_json (NameAndOccurrence): A list of names from the replacement json.

        """

        _names_in_knowledge_base = [_name for _name in names_in_knowledge_base if not (
                                                KatakanaUtil.is_more_punctuation_than_japanese(_name.name) or 
                                                KatakanaUtil.is_actual_word(_name.name) or 
                                                KatakanaUtil.is_partially_english(_name.name) or
                                                KatakanaUtil.is_repeating_sequence(_name.name))]
        
        _names_in_text_to_index = [_name for _name in names_in_text_to_index if not (
                                                KatakanaUtil.is_more_punctuation_than_japanese(_name.name) or 
                                                KatakanaUtil.is_actual_word(_name.name) or 
                                                KatakanaUtil.is_partially_english(_name.name) or
                                                KatakanaUtil.is_repeating_sequence(_name.name))]
        
        _names_in_replacement_json = [_name for _name in names_in_replacement_json if not (
                                                KatakanaUtil.is_more_punctuation_than_japanese(_name.name) or 
                                                KatakanaUtil.is_actual_word(_name.name) or 
                                                KatakanaUtil.is_partially_english(_name.name) or
                                                KatakanaUtil.is_repeating_sequence(_name.name))]

        return _names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json
    
##-------------------start-of-trim_honorifics()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def _trim_honorifics(names_in_knowledge_base:typing.List[NameAndOccurrence], 
                        names_in_text_to_index:typing.List[NameAndOccurrence], 
                        names_in_replacement_json:typing.List[NameAndOccurrence]) -> typing.Tuple[typing.List[NameAndOccurrence], typing.List[NameAndOccurrence], typing.List[NameAndOccurrence]]:
        
        """
        
        Trims honorifics from names.

        Parameters:
        names_in_knowledge_base (NameAndOccurrence): A list of names from the knowledge base.
        names_in_text_to_index (NameAndOccurrence): A list of names from the text to index.
        names_in_replacement_json (NameAndOccurrence): A list of names from the replacement json.

        Returns:
        names_in_knowledge_base (NameAndOccurrence): A list of names from the knowledge base.
        names_in_text_to_index (NameAndOccurrence): A list of names from the text to index.
        names_in_replacement_json (NameAndOccurrence): A list of names from the replacement json.

        """

        ## both kudasai and fukuin jsons have honorifics
        _honorifics = Indexer._replacement_json.get('honorifics', [])

        for _honorific in _honorifics:
            _names_in_knowledge_base = [NameAndOccurrence(_name.name.replace(_honorific, ""), _name.occurrence) for _name in names_in_knowledge_base]
            _names_in_text_to_index = [NameAndOccurrence(_name.name.replace(_honorific, ""), _name.occurrence) for _name in names_in_text_to_index]
            _names_in_replacement_json = [NameAndOccurrence(_name.name.replace(_honorific, ""), _name.occurrence) for _name in names_in_replacement_json]

        return _names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json
    
##-------------------start-of-is_name_in_other_sources()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _is_name_in_other_sources(name:str, all_names:typing.Set[str]) -> bool:

        """

        Checks if a name is in the knowledge base or replacement json.

        Parameters:
        name (str): The name to check.
        all_names (set): A set of all names.

        Returns:
        bool: True if the name is in the knowledge base or replacement json, False otherwise.

        """

        return any(_other_name in name for _other_name in all_names)
    
##-------------------start-of-index()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def index(text_to_index:str, 
              knowledge_base:str, 
              replacement_json:typing.Union[str, dict],
              blacklist:typing.List[str] = [],
              discard_ner_objects:bool = True
              ) -> typing.Tuple[typing.List[NameAndOccurrence], str]:

        """
        
        Determines which names in the text to index are not in the knowledge base or replacement json and returns them as a list of NameAndOccurrence named tuples.

        Returns a tuple of tuples. That tuple has the name itself and the occurrence of the name that was flagged.

        Parameters:
        text_to_index (str) : The text to index. Can be a path to a text file, or just the text itself.
        knowledge_base (str) : The knowledge base. Can be a path to a directory containing text files, a path to a text file, or just the text itself.
        replacement_json (str) : The replacement json. Can be a path to a json, or as the json itself.
        blacklist (list - str) : A list of strings to ignore.
        discard_ner_objects (bool - default: True) : Whether to discard the spacy NER object after processing. This is because having the NER object continuously in memory can be memory intensive.
        
        Returns:
        new_names (NameAndOccurrence): A list of names that are not in the knowledge base or replacement_json. (NameAndOccurrence is a named tuple with the fields name and occurrence).
        indexing_log (str): Log of the indexing process (names that were flagged as unique 'names' and which occurrence they were flagged at).
        
        """

        _time_start = time.time()
    
        try:

            if(Indexer._ner is None):
                Indexer._ner = spacy.load("ja_core_news_lg")

        except Exception:
            raise SpacyModelNotFound

        if(len(blacklist) > 0):
            Indexer._blacklisted_names = blacklist

        new_names:typing.List[NameAndOccurrence] = []

        Indexer._load_static_data(text_to_index, knowledge_base, replacement_json)

        _names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json = Indexer._get_names_from_all_sources()

        _names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json = Indexer._perform_further_elimination(_names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json)

        if(replacement_json):
            _names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json = Indexer._trim_honorifics(_names_in_knowledge_base, _names_in_text_to_index, _names_in_replacement_json)

        _names_in_knowledge_base = set(_name.name for _name in _names_in_knowledge_base)
        _names_in_replacement_json = set(_name.name for _name in _names_in_replacement_json)

        _all_names = _names_in_knowledge_base | _names_in_replacement_json

        for _name in _names_in_text_to_index:
            if(not Indexer._is_name_in_other_sources(_name.name, _all_names)):
                new_names.append(_name)
                Indexer.indexing_log += (f"Name: {_name.name} Occurrence: {_name.occurrence} was flagged as a unique 'name'\n")

        if(discard_ner_objects):
            Indexer._ner = None
            del Indexer._ner
            import gc
            gc.collect()

        _time_end = time.time()

        Indexer.indexing_log += "\nIgnored Strings: " + str(Indexer._blacklisted_names)

        Indexer.indexing_log += "\nTotal Unique 'Names'  : " + \
            str(len(new_names))
        Indexer.indexing_log += "\nTime Elapsed : " + \
            _get_elapsed_time(_time_start, _time_end)

        return new_names, Indexer.indexing_log