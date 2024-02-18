## built-in libraries
import itertools
import typing
import time
import json

## third-party libraries
import spacy

## custom modules
from .katakana_util import KatakanaUtil
from .util import validate_replacement_json, get_elapsed_time, Name, ReplacementType, kudasai_blank_json, fukuin_blank_json, kudasai_replacement_rules
from .exceptions import  InvalidReplacementJsonName, InvalidReplacementJsonPath

# -------------------start-of-Kairyou---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Kairyou:

    """

    The global Kairyou client for preprocessing Japanese text.

    """

    ## The dictionary containing the rules for preprocessing.
    replacement_json:dict = {}

    ## The text to be preprocessed. Preprocessing is in-place.
    text_to_preprocess = ""

    ## These are static vars that will be reset every time preprocess is called.
    preprocessing_log = ""
    error_log = ""
    total_replacements = 0

    ## How japanese names are separated in the japanese text
    JAPANESE_NAME_SEPARATORS = ["・", ""]

    ##------------------------/

    ## Supported types of json files.
    ## Kudasai is kairyou's native json format. See https://github.com/Bikatr7/Kairyou/blob/main/examples/blank_kudasai.json
    ## Fukuin is the format used by the original onegai processor and kroatoan's Fukuin. See https://github.com/Bikatr7/Kairyou/tree/main/examples/blank_fukuin.json
    json_type:typing.Literal["kudasai", "fukuin"] = "kudasai"

    replacement_rules:typing.List = kudasai_replacement_rules

    #----------------------------/

    ## The spacy NER model used for enhanced replacement checking.
    ner = spacy.load("ja_core_news_lg")
    
##-------------------start-of-reset_globals()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def reset_globals() -> None:

        """

        Resets the global variables.

        Resets both logs, the total replacements, json type, and replacement rules to their default values: Empty strings, 0, and Kudasai type respectively.

        """

        Kairyou.preprocessing_log = ""
        Kairyou.error_log = ""

        Kairyou.total_replacements = 0

        Kairyou.json_type = "kudasai"
 
        Kairyou.replacement_rules = kudasai_replacement_rules

##-------------------start-of-preprocess()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def preprocess(text_to_preprocess:str, replacement_json:typing.Union[dict,str], persist:bool = False) -> typing.Tuple[str, str, str]:

        """

        Preprocesses the text using the replacement json.

        Using preprocess will effectively reset the global Kairyou client unless persist is set to True.

        Will skip the preprocessing if the replacement json is blank.

        Parameters:
        text_to_preprocess (str) : The text to be preprocessed.
        replacement_json (dict | str) : The rules for preprocessing. Can be a dictionary or a path to a json file.
        persist (bool | optional | default=False) : If True, the global Kairyou client will not be reset upon starting the function.

        Returns:
        Kairyou.text_to_preprocess (str) : The preprocessed text.
        Kairyou.preprocessing_log (str) : The log of replacements made.
        Kairyou.error_log (str) : The log of errors encountered (if any).

        Raises:
        ValueError : If the text to be preprocessed is empty.

        """

        ## If the replacement json is blank, skip the preprocessing.
        if(replacement_json == kudasai_blank_json or replacement_json == fukuin_blank_json):
            return text_to_preprocess, "Skipped", "Skipped"

        if(not persist):
            Kairyou.reset_globals()

        if(len(text_to_preprocess) != 0):
            Kairyou.text_to_preprocess = text_to_preprocess

            if(isinstance(replacement_json, str)):
                ## try to load the replacement json file
                try:

                    with open(replacement_json, 'r', encoding='utf-8') as file: ## type: ignore (also a string)
                        replacement_json = json.load(file)

                except Exception:
                    raise InvalidReplacementJsonPath(replacement_json) ## type: ignore (it's a string)
            
            Kairyou.replacement_json = replacement_json ## type: ignore (it's a dict)

            Kairyou.json_type, Kairyou.replacement_rules = validate_replacement_json(Kairyou.replacement_json)

        else:
            raise ValueError("The text to be preprocessed cannot be empty.")

        replaced_names = dict()

        time_start = time.time()

        Kairyou.replace_non_katakana(replaced_names)
        Kairyou.replace_katakana(replaced_names)

        time_end = time.time()

        Kairyou.preprocessing_log += "\nTotal Replacements  : " + \
            str(Kairyou.total_replacements)
        Kairyou.preprocessing_log += "\nTime Elapsed : " + \
            get_elapsed_time(time_start, time_end)

        return Kairyou.text_to_preprocess, Kairyou.preprocessing_log, Kairyou.error_log

##-------------------start-of-replace_non_katakana()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_non_katakana(replaced_names: dict) -> None:

        """

        Handles non-katakana replacements.

        Parameters:
        replaced_names (dict - str) : Names that have been replaced.

        """

        ## for non-katakana replacements
        for rule in Kairyou.replacement_rules:

            title, json_key, is_name, replace_name_param, honorific_type = rule

            if(is_name == True):

                try:
                    for eng, jap in Kairyou.replacement_json[json_key].items():

                        ## makes jap entries into a list if not already
                        if(isinstance(jap, list) == False):
                            jap = [jap]

                        current_name = Name(" ".join(jap), eng)

                        ## katakana is replaced at the end
                        if(KatakanaUtil.is_katakana_only(current_name.jap)):
                            continue

                        Kairyou.replace_name(current_name, replace_name_param, honorific_type,
                                             replaced_names, json_key, is_potential_name=True, is_katakana=False)

                except Exception as E:
                    Kairyou.error_log += "Issue with the following key : " + json_key + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(E)
                    continue

            else:
                try:
                    for jap, eng in Kairyou.replacement_json[json_key].items():

                        num_replacements = Kairyou.replace_single_word(
                            jap, eng, is_potential_name=False)

                        if(num_replacements > 0):
                            Kairyou.preprocessing_log += str(jap) + " → " + str(
                                eng) + " : " + str(num_replacements) + "\n"

                except Exception as E:
                    Kairyou.error_log += "Issue with the following key : " + json_key + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(E)
                    continue

##-------------------start-of-replace_katakana()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_katakana(replaced_names: dict) -> None:

        """

        Handles katakana replacements.

        Parameters:
        replaced_names (dict - str) : Names we have replaced.

        """

        katakana_entries = []

        for rule in Kairyou.replacement_rules:

            title, json_key, is_name, replace_name_param, honorific_type = rule

            if(is_name == True):

                for eng, jap in Kairyou.replacement_json[json_key].items():

                    ## makes jap entries into a list if not already
                    if(isinstance(jap, list) == False):
                        jap = [jap]

                    current_name = Name(" ".join(jap), eng)

                    if(KatakanaUtil.is_katakana_only(current_name.jap) and not KatakanaUtil.is_actual_word(current_name.jap)):
                        katakana_entries.append(
                            (current_name, replace_name_param, honorific_type, json_key))
            else:

                for jap, eng in Kairyou.replacement_json[json_key].items():

                    if(KatakanaUtil.is_katakana_only(jap) and not KatakanaUtil.is_actual_word(jap)):
                        katakana_entries.append((jap, eng))

        ## Sort the katakana entries by the length of Japanese phrases in descending order
        katakana_entries.sort(key=lambda entry: len(
            entry[0].jap if isinstance(entry[0], Name) else entry[0]), reverse=True)

        ## Replace katakana names and words
        for entry in katakana_entries:

            ## names
            if(isinstance(entry[0], Name)):

                current_name, replace_name_param, honorific_type, json_key = entry

                try:
                    Kairyou.replace_name(current_name, replace_name_param, honorific_type,
                                         replaced_names, json_key, is_potential_name=True, is_katakana=True)

                except Exception as E:
                    Kairyou.error_log += "Issue with the following key : " + json_key + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(E)
                    continue
            else:

                ## Handling non-names
                jap, eng = entry

                try:
                    num_replacements = Kairyou.replace_single_word(
                        jap, eng, is_potential_name=False, is_katakana=True)

                    if (num_replacements > 0):
                        Kairyou.preprocessing_log += str(jap) + " → " + str(
                            eng) + " : " + str(num_replacements) + "\n"

                except Exception as E:
                    Kairyou.error_log += "Issue with the word : " + jap + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(E)
                    continue

##-------------------start-of-yield_name_replacements()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def yield_name_replacements(Name: Name, replace_type: ReplacementType, honorific_type: ReplacementType) -> typing.Generator[tuple[str, str, bool], None, None]:

        """

        Generates tuples of English and Japanese names to be replaced, along with a boolean indicating whether honorifics should be kept or removed.

        Parameters:
        Name (object - Name) : represents a japanese name along with its english equivalent.
        replace_type  (object - ReplacementType) : how a name should be replaced.
        honorific_type (object - ReplacementType) : how a honorific_type should be replaced.

        Returns:
        tuple (string, string, bool) : tuple containing the japanese name, english name, and a boolean indicating whether honorifics should be kept or removed.

        tuple is wrapped in a generator along with two None values. No, I don't know why.

        """

        japanese_names = Name.jap.split(" ")
        english_names = Name.eng.split(" ")

        ## if the lengths of the names don't match, the entire Name is fucked.
        try:

            assert len(japanese_names) == len(english_names)

        except AssertionError:
            raise InvalidReplacementJsonName(Name)

        if(ReplacementType.FULL_NAME in replace_type):
            indices = range(len(japanese_names))
            ## create a chain of combinations of indices, starting with combinations of length 2 up to the length of indices
            combinations = itertools.chain(
                *(itertools.combinations(indices, i) for i in range(2, len(indices)+1)))

            for comb in combinations:
                for separator in Kairyou.JAPANESE_NAME_SEPARATORS:
                    yield (" ".join(map(lambda i: english_names[i], comb)),
                           separator.join(
                               map(lambda i: japanese_names[i], comb)),
                           ReplacementType.FULL_NAME in honorific_type)

        if(ReplacementType.FIRST_NAME in replace_type):
            yield(english_names[0],
                   f'{japanese_names[0]}',
                   ReplacementType.FIRST_NAME in honorific_type)

        if(ReplacementType.LAST_NAME in replace_type):
            yield(english_names[-1],
                   f'{japanese_names[-1]}',
                   ReplacementType.LAST_NAME in honorific_type)

# -------------------start-of-replace_single_word()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_single_word(word: str, replacement: str, is_potential_name: bool, is_katakana: bool = False) -> int:

        """

        Replaces a single word in the Japanese text, with an additional check for Katakana words.

        The function is extremely picky with katakana in general.

        Parameters:
        word (string) : The word to be replaced.
        replacement (string) : The replacement for the word.
        is_katakana (bool | optional | default=false) : Indicates if the word is in Katakana.

        Returns:
        num_occurrences (int) : The number of occurrences of the word replaced.

        """

        num_occurrences = 0

        if(is_katakana):

            ## Skip replacement if it's an actual word.
            if(KatakanaUtil.is_actual_word(word)):
                return 0

            else:

                ## Use NER to ensure we're not replacing a proper name that's not in our list of Katakana words.
                if (is_potential_name):
                    Kairyou.perform_enhanced_replace(word, replacement)

                else:
                    num_occurrences = Kairyou.text_to_preprocess.count(word)
                    if (num_occurrences > 0):
                        Kairyou.text_to_preprocess = Kairyou.text_to_preprocess.replace(
                            word, replacement)

        else:
            num_occurrences = Kairyou.text_to_preprocess.count(word)
            if (num_occurrences > 0):
                Kairyou.text_to_preprocess = Kairyou.text_to_preprocess.replace(
                    word, replacement)

        Kairyou.total_replacements += num_occurrences

        return num_occurrences

# -------------------start-of-replace_name()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_name(Name: Name, replace_type: ReplacementType, honorific_type: ReplacementType, replaced_names: dict, json_key: str, is_potential_name: bool, is_katakana: bool) -> None:

        """

        Replaces names in the japanese text based off of tuples returned by yield_name_replacements.

        Parameters:
        Name (object - Name)  : represents a japanese name along with its english equivalent.
        replace_type  (object - ReplacementType) : how a name should be replaced.
        honorific_type (object - ReplacementType) : how a honorific should be replaced.
        replaced_names (dict - string) : a dict of replaced names and their occurrences.
        is_katakana (bool) : Indicates if the name is in Katakana.

        """

        for eng, jap, no_honor in Kairyou.yield_name_replacements(Name, replace_type, honorific_type):

            ## Skip the replacement if this name has already been processed.
            if (jap in replaced_names):
                continue

            replacement_data = dict()

            ## Process honorifics if necessary
            ## Both fukuin and kudasai jsons have the honorifics key
            for honor, honorific_english in Kairyou.replacement_json['honorifics'].items():
                replacement_data[honorific_english] = Kairyou.replace_single_word(
                    f'{jap}{honor}',
                    f'{eng}-{honorific_english}',

                    # if honorifics, don't worry about additonal checking
                    is_potential_name=False,
                    is_katakana=False,
                )

            if(is_katakana):
                ## Skip replacement if it's an actual Katakana word.
                if(KatakanaUtil.is_actual_word(jap)):
                    continue
                else:
                    ## Perform enhanced replacement check with NER
                    replacement_data['NA'] = Kairyou.perform_enhanced_replace(
                        jap, eng)

            ## If the name does not have honorific and isn't a known Katakana word, or we aren't checking for Katakana
            if(no_honor):
                ## needs to be kudasai json type to have that key, so this'll short-circuit that check, can also just be a single kanji
                if(Kairyou.json_type == "kudasai" and json_key == "enhanced_check_whitelist" or len(jap) == 1):
                    replacement_data['NA'] = Kairyou.perform_enhanced_replace(
                        jap, eng)

                else:
                    replacement_data['NA'] = Kairyou.replace_single_word(
                        jap, eng, is_potential_name, is_katakana)

            ## Sum the total replacements for this name
            total = sum(replacement_data.values())

            replaced_names[jap] = total

            ## If no replacements occurred, skip the logging
            if(total == 0):
                continue

            ## Log the replacements
            Kairyou.preprocessing_log += f'{eng} : {total} ('
            Kairyou.preprocessing_log += ', '.join(
                [f'{key}-{value}' for key, value in replacement_data.items() if value > 0]) + ')\n'

##-------------------start-of-perform_enhanced_replace()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def perform_enhanced_replace(jap: str, replacement: str) -> int:
        
        """

        Uses NER (Named Entity Recognition) from the spacy module to replace names that need to be more carefully replaced, such as single kanji, katakana names, or those placed in the user whitelist.

        May miss true positives, but should not replace false positives.

        Parameters:
        jap (str) : Japanese to be replaced.
        replacement (str) : The replacement for the Japanese

        Returns:
        jap_replace_count (int) : How many japanese replacements that were made.

        """

        i = 0
        jap_replace_count = 0

        jap_lines = Kairyou.text_to_preprocess.split('\n')

        while (i < len(jap_lines)):
            if (jap in jap_lines[i]):

                sentence = Kairyou.ner(jap_lines[i])

                for entity in sentence.ents:
                    if (entity.text == jap and entity.label_ == "PERSON"):
                        jap_replace_count += 1
                        jap_lines[i] = jap_lines[i][:entity.start_char] + \
                            replacement + jap_lines[i][entity.end_char:]

            i += 1

        Kairyou.text_to_preprocess = '\n'.join(jap_lines)
        Kairyou.total_replacements += jap_replace_count

        return jap_replace_count
