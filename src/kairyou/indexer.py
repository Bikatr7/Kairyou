## built-in libraries
import os
import json
import typing

## third-party libraries
import spacy

## custom modules
from .util import validate_replacement_json

class Indexer:

    replacement_json:dict

    json_type:typing.Literal["kudasai", "fukuin"]

    text_to_index:str

    knowledge_base:typing.List[str]

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

            entries.extend(Indexer.replacement_json[key])

        return list(set(entries))        

##-------------------start-of-get_names_from_all_sources()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_names_from_all_sources() -> typing.List[typing.List]:
        
        """
        
        Fetches all names from the knowledge_base, text_to_index, and replacement_json and returns them as a list.

        """

        names_in_knowledge_base = []
        names_in_text_to_index = []
        names_in_replacement_json = Indexer.get_names_from_replacement_json()

        for entry in Indexer.knowledge_base:
            
            entry = entry.split("\n")

            for line in entry:
                sentence = Indexer.ner(line)
                for entity in sentence.ents:
                    if(entity.label_ == "PERSON"):
                        names_in_knowledge_base.append(entity.text)

        for entry in Indexer.text_to_index.split("\n"):
            sentence = Indexer.ner(entry)
            for entity in sentence.ents:
                if(entity.label_ == "PERSON"):
                    names_in_text_to_index.append(entity.text)

        names_in_knowledge_base = list(set(names_in_knowledge_base))
        names_in_text_to_index = list(set(names_in_text_to_index))

        return [names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json]
    
##-------------------start-of-index()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def index(text_to_index, knowledge_base, replacement_json):

        """
        
        Indexes the text_to_index using the knowledge_base and replacement_json.

        """

        Indexer.load_static_data(text_to_index, knowledge_base, replacement_json)

        names_in_knowledge_base, names_in_text_to_index, names_in_replacement_json = Indexer.get_names_from_all_sources()

        for name in names_in_text_to_index:
            
            if(name not in names_in_knowledge_base and name not in names_in_replacement_json):
                print(f"Name {name} not found in knowledge_base or replacement_json. Please add it to one of these sources.")



