## Copyright 2024 Kaden Bilyeu (Bikatr7) (https://github.com/Bikatr7) (https://github.com/Bikatr7/Kairyou)
## Use of this source code is governed by a GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import itertools
import typing
import time
import json
import regex

## third-party libraries
import spacy

## custom modules
from .katakana_util import KatakanaUtil
from .util import _validate_replacement_json, _get_elapsed_time, Name, ReplacementType, _kudasai_blank_json, _fukuin_blank_json, _kudasai_replacement_rules
from .exceptions import  InvalidReplacementJsonName, InvalidReplacementJsonPath, InvalidPreprocessingText, SpacyModelNotFound

# -------------------start-of-Kairyou---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Kairyou:

    """

    The global Kairyou client for preprocessing Japanese text.

    """

    ## The dictionary containing the rules for preprocessing.
    _replacement_json:dict = {}

    ## The text to be preprocessed. Preprocessing is in-place.
    text_to_preprocess = ""

    ## These are static vars that will be reset every time preprocess is called.
    preprocessing_log = ""
    error_log = ""

    _total_replacements = 0

    ## How japanese names are separated in the japanese text
    _JAPANESE_NAME_SEPARATORS = ["・", ""]

    ##------------------------/

    ## Supported types of json files.
    ## Kudasai is kairyou's native json format. See https://github.com/Bikatr7/Kairyou/blob/main/examples/blank_kudasai.json
    ## Fukuin is the format used by the original onegai processor and kroatoan's Fukuin. See https://github.com/Bikatr7/Kairyou/tree/main/examples/blank_fukuin.json
    _json_type:typing.Literal["kudasai", "fukuin"] = "kudasai"

    _replacement_rules:typing.List = _kudasai_replacement_rules

    #----------------------------/

    _ner:spacy.language.Language | None = None

    _add_closing_period = False

##-------------------start-of-_reset_globals()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _reset_globals() -> None:

        """

        Resets the global variables.

        Resets both logs, the total replacements, json type, and replacement rules to their default values: Empty strings, 0, and Kudasai type respectively.

        """

        Kairyou.text_to_preprocess = ""
        Kairyou.preprocessing_log = ""
        Kairyou.error_log = ""

        Kairyou._total_replacements = 0

        Kairyou._json_type = "kudasai"
 
        Kairyou._replacement_rules = _kudasai_replacement_rules

##-------------------start-of-preprocess()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def preprocess(text_to_preprocess:str, replacement_json:typing.Union[dict,str], persist:bool = False, discard_ner_objects:bool = True, add_closing_period:bool = False) -> typing.Tuple[str, str, str]:

        """

        Preprocesses the text using the replacement json.

        Using preprocess will effectively reset the global Kairyou client unless persist is set to True.

        Will skip the preprocessing if the replacement json is blank.

        Parameters:
        text_to_preprocess (str) : The text to be preprocessed.
        replacement_json (dict | str) : The rules for preprocessing. Can be a dictionary or a path to a json file.
        persist (bool | optional | default=False) : If True, the global Kairyou client will not be reset upon starting the function.
        discard_ner_objects (bool | optional | default=True) : Whether to discard the spacy NER object after processing. This is because having the NER object continuously in memory can be memory intensive.
        add_closing_period (bool | optional | default=False) : Whether to add closing periods (。) before 」 where missing.
        Returns:
        Kairyou.text_to_preprocess (str) : The preprocessed text.
        Kairyou.preprocessing_log (str) : The log of replacements made.
        Kairyou.error_log (str) : The log of errors encountered (if any).

        Raises:
        ValueError : If the text to be preprocessed is empty.

        """

        Kairyou._add_closing_period = add_closing_period

        ## The spacy NER model used for enhanced replacement checking.
        try:

            if(Kairyou._ner is None):
                Kairyou._ner = spacy.load("ja_core_news_lg")

        except Exception:
            raise SpacyModelNotFound

        ## If the replacement json is blank, skip the preprocessing.
        if(replacement_json == _kudasai_blank_json or replacement_json == _fukuin_blank_json):
            return text_to_preprocess, "Skipped", ""

        if(not persist):
            Kairyou._reset_globals()

        if(len(text_to_preprocess) != 0):
            if(add_closing_period):
                text_to_preprocess = Kairyou._add_missing_periods(text_to_preprocess)
            
            Kairyou.text_to_preprocess = text_to_preprocess

            if(isinstance(replacement_json, str)):
                ## try to load the replacement json file
                try:

                    with open(replacement_json, 'r', encoding='utf-8') as file: ## type: ignore (also a string)
                        replacement_json = json.load(file)

                except Exception:
                    raise InvalidReplacementJsonPath(replacement_json) ## type: ignore (it's a string)
            
            Kairyou._replacement_json = replacement_json ## type: ignore (it's a dict)

            Kairyou._json_type, Kairyou._replacement_rules = _validate_replacement_json(Kairyou._replacement_json)

        else:
            raise InvalidPreprocessingText("Text to be preprocessed is empty.")

        _replaced_names = dict()

        _time_start = time.time()

        Kairyou._replace_non_katakana(_replaced_names)
        Kairyou._replace_katakana(_replaced_names)

        Kairyou._perform_postprocessing()

        if(discard_ner_objects):
            Kairyou._ner = None
            del Kairyou._ner
            import gc
            gc.collect()

        _time_end = time.time()

        Kairyou.preprocessing_log += "\nTotal Replacements  : " + \
            str(Kairyou._total_replacements)
        Kairyou.preprocessing_log += "\nTime Elapsed : " + \
            _get_elapsed_time(_time_start, _time_end)

        return Kairyou.text_to_preprocess, Kairyou.preprocessing_log, Kairyou.error_log
    
##-------------------start-of-_perform_postprocessing()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def _perform_postprocessing() -> None:

        """

        Performs postprocessing on the text after the replacements have been made.

        """

        Kairyou._perform_missing_space_correction()

##-------------------start-of-_perform_missing_space_correction()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _perform_missing_space_correction() -> None:

        """

        Sometimes, two individual names maybe be replaced separately, rather than as a single name, leading to a missing space. This function corrects that.
        Seems to occur rarely, but better to have it than not. Only occurs in Kudasai type jsons.

        """

        if(Kairyou._json_type != "kudasai"):
            return 

        english_in_text = [(match.group(), match.start()) for match in regex.finditer(r'\p{Latin}+', Kairyou.text_to_preprocess)]
        full_names = [name for name in Kairyou._replacement_json['full_names'].keys()]

        for english, start in english_in_text:
            for full_name in full_names:
                first_name, last_name = full_name.split(" ")
        
                if(first_name in Kairyou.text_to_preprocess[start:] and last_name in Kairyou.text_to_preprocess[start:]):
                    Kairyou.text_to_preprocess = Kairyou.text_to_preprocess.replace(first_name + last_name, first_name + " " + last_name)
                    pass
        
##-------------------start-of-_replace_non_katakana()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _replace_non_katakana(replaced_names:dict) -> None:

        """

        Handles non-katakana replacements.

        Parameters:
        replaced_names (dict - str) : Names that have been replaced.

        """

        ## for non-katakana replacements
        for _rule in Kairyou._replacement_rules:

            ## unpack the rule
            _, _json_key, _is_name, _replace_name_param, _honorific_type = _rule

            if(_is_name == True):

                try:
                    for _eng, _jap in Kairyou._replacement_json[_json_key].items():

                        ## makes jap entries into a list if not already
                        if(isinstance(_jap, list) == False):
                            _jap = [_jap]

                        _current_name = Name(" ".join(_jap), _eng)

                        ## katakana is replaced at the end
                        if(KatakanaUtil.is_katakana_only(_current_name.jap)):
                            continue

                        Kairyou._replace_name(_current_name, _replace_name_param, _honorific_type,
                                             replaced_names, _json_key, is_potential_name=True, is_katakana=False)

                except Exception as _e:
                    Kairyou.error_log += "Issue with the following key : " + _json_key + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(_e)
                    continue

            else:
                try:
                    for _jap, _eng in Kairyou._replacement_json[_json_key].items():

                        _num_replacements = Kairyou._replace_single_word(
                            _jap, _eng, is_potential_name=False)

                        if(_num_replacements > 0):
                            Kairyou.preprocessing_log += str(_jap) + " → " + str(
                                _eng) + " : " + str(_num_replacements) + "\n"

                except Exception as _e:
                    Kairyou.error_log += "Issue with the following key : " + _json_key + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(_e)
                    continue

##-------------------start-of-_replace_katakana()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _replace_katakana(replaced_names:dict) -> None:

        """

        Handles katakana replacements.

        Parameters:
        replaced_names (dict - str) : Names we have replaced.

        """

        _katakana_entries = []

        for _rule in Kairyou._replacement_rules:

            ## unpack the rule
            _, _json_key, _is_name, _replace_name_param, _honorific_type = _rule

            if(_is_name == True):

                for _eng, _jap in Kairyou._replacement_json[_json_key].items():

                    ## makes jap entries into a list if not already
                    if(isinstance(_jap, list) == False):
                        _jap = [_jap]

                    _current_name = Name(" ".join(_jap), _eng)

                    if(KatakanaUtil.is_katakana_only(_current_name.jap) and not KatakanaUtil.is_actual_word(_current_name.jap)):
                        _katakana_entries.append(
                            (_current_name, _replace_name_param, _honorific_type, _json_key))
            else:

                for _jap, _eng in Kairyou._replacement_json[_json_key].items():

                    if(KatakanaUtil.is_katakana_only(_jap) and not KatakanaUtil.is_actual_word(_jap)):
                        _katakana_entries.append((_jap, _eng))

        ## Sort the katakana entries by the length of Japanese phrases in descending order
        _katakana_entries.sort(key=lambda _entry: len(
            _entry[0].jap if isinstance(_entry[0], Name) else _entry[0]), reverse=True)

        ## Replace katakana names and words
        for _entry in _katakana_entries:

            ## names
            if(isinstance(_entry[0], Name)):

                _current_name, _replace_name_param, _honorific_type, _json_key = _entry

                try:
                    Kairyou._replace_name(_current_name, _replace_name_param, _honorific_type,
                                         replaced_names, _json_key, is_potential_name=True, is_katakana=True)

                except Exception as _e:
                    Kairyou.error_log += "Issue with the following key : " + _json_key + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(_e)
                    continue
            else:

                ## Handling non-names
                _jap, _eng = _entry

                try:
                    _num_replacements = Kairyou._replace_single_word(
                        _jap, _eng, is_potential_name=False, is_katakana=True)

                    if(_num_replacements > 0):
                        Kairyou.preprocessing_log += str(_jap) + " → " + str(
                            _eng) + " : " + str(_num_replacements) + "\n"

                except Exception as _e:
                    Kairyou.error_log += "Issue with the word : " + _jap + "\n"
                    Kairyou.error_log += "Error is as follows : " + str(_e)
                    continue

##-------------------start-of-_yield_name_replacements()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _yield_name_replacements(name:Name, replace_type:ReplacementType, honorific_type:ReplacementType) -> typing.Generator[tuple[str, str, bool], None, None]:

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

        _japanese_names = name.jap.split(" ")
        _english_names = name.eng.split(" ")

        ## if the lengths of the names don't match, the entire Name is fucked.
        try:

            assert len(_japanese_names) == len(_english_names)

        except AssertionError:
            raise InvalidReplacementJsonName(name)

        if(ReplacementType.FULL_NAME in replace_type):
            _indices = range(len(_japanese_names))
            ## create a chain of combinations of indices, starting with combinations of length 2 up to the length of indices
            _combinations = itertools.chain(
                *(itertools.combinations(_indices, i) for i in range(2, len(_indices)+1)))

            for _comb in _combinations:
                for _separator in Kairyou._JAPANESE_NAME_SEPARATORS:
                    yield (" ".join(map(lambda i: _english_names[i], _comb)),
                           _separator.join(
                               map(lambda i: _japanese_names[i], _comb)),
                           ReplacementType.FULL_NAME in honorific_type)

        if(ReplacementType.FIRST_NAME in replace_type):
            yield(_english_names[0],
                   f'{_japanese_names[0]}',
                   ReplacementType.FIRST_NAME in honorific_type)

        if(ReplacementType.LAST_NAME in replace_type):
            yield(_english_names[-1],
                   f'{_japanese_names[-1]}',
                   ReplacementType.LAST_NAME in honorific_type)

# -------------------start-of-_replace_single_word()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _replace_single_word(word:str, replacement:str, is_potential_name:bool, is_katakana:bool = False) -> int:

        """

        Replaces a single word in the Japanese text, with an additional check for Katakana words.

        The function is extremely picky with katakana in general.

        Parameters:
        word (string) : The word to be replaced.
        replacement (string) : The replacement for the word.
        is_potential_name (bool) : Indicates if the word is a potential name.
        is_katakana (bool | optional | default=false) : Indicates if the word is in Katakana.

        Returns:
        _num_occurrences (int) : The number of occurrences of the word replaced.

        """

        _num_occurrences = 0

        if(is_katakana):

            ## Skip replacement if it's an actual word.
            if(KatakanaUtil.is_actual_word(word)):
                return 0

            else:

                ## Use NER to ensure we're not replacing a proper name that's not in our list of Katakana words.
                if(is_potential_name):
                    Kairyou._perform_enhanced_replace(word, replacement)

                else:
                    _num_occurrences = Kairyou.text_to_preprocess.count(word)
                    if(_num_occurrences > 0):
                        Kairyou.text_to_preprocess = Kairyou.text_to_preprocess.replace(
                            word, replacement)

        else:
            _num_occurrences = Kairyou.text_to_preprocess.count(word)
            if(_num_occurrences > 0):
                Kairyou.text_to_preprocess = Kairyou.text_to_preprocess.replace(
                    word, replacement)

        Kairyou._total_replacements += _num_occurrences

        return _num_occurrences

# -------------------start-of-_replace_name()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _replace_name(name:Name, replace_type:ReplacementType, honorific_type:ReplacementType, replaced_names:dict, json_key:str, is_potential_name:bool, is_katakana:bool) -> None:

        """

        Replaces names in the japanese text based off of tuples returned by _yield_name_replacements.

        Parameters:
        name (object - Name)  : represents a japanese name along with its english equivalent.
        replace_type  (object - ReplacementType) : how a name should be replaced.
        honorific_type (object - ReplacementType) : how a honorific should be replaced.
        replaced_names (dict - string) : a dict of replaced names and their occurrences.
        is_katakana (bool) : Indicates if the name is in Katakana.

        """

        for _eng, _jap, _no_honor in Kairyou._yield_name_replacements(name, replace_type, honorific_type):

            ## Skip the replacement if this name has already been processed.
            if(_jap in replaced_names):
                continue

            _replacement_data = dict()

            ## Process honorifics if necessary
            ## Both fukuin and kudasai jsons have the honorifics key
            for _honor, _honorific_english in Kairyou._replacement_json['honorifics'].items():
                _replacement_data[_honorific_english] = Kairyou._replace_single_word(
                    f'{_jap}{_honor}',
                    f'{_eng}-{_honorific_english}',

                    # if honorifics, don't worry about additonal checking
                    is_potential_name=False,
                    is_katakana=False,
                )

            if(is_katakana):
                ## Skip replacement if it's an actual Katakana word.
                if(KatakanaUtil.is_actual_word(_jap)):
                    continue
                else:
                    ## Perform enhanced replacement check with NER
                    _replacement_data['NA'] = Kairyou._perform_enhanced_replace(
                        _jap, _eng)

            ## If the name does not have honorific and isn't a known Katakana word, or we aren't checking for Katakana
            if(_no_honor):
                ## needs to be kudasai json type to have that key, so this'll short-circuit that check, can also just be a single kanji
                if(Kairyou._json_type == "kudasai" and json_key == "enhanced_check_whitelist" or len(_jap) == 1):
                    _replacement_data['NA'] = Kairyou._perform_enhanced_replace(
                        _jap, _eng)

                else:
                    _replacement_data['NA'] = Kairyou._replace_single_word(
                        _jap, _eng, is_potential_name, is_katakana)

            ## Sum the total replacements for this name
            _total = sum(_replacement_data.values())

            replaced_names[_jap] = _total

            ## If no replacements occurred, skip the logging
            if(_total == 0):
                continue

            ## Log the replacements
            Kairyou.preprocessing_log += f'{_eng} : {_total} ('
            Kairyou.preprocessing_log += ', '.join(
                [f'{_key}-{_value}' for _key, _value in _replacement_data.items() if _value > 0]) + ')\n'

##-------------------start-of-_perform_enhanced_replace()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _perform_enhanced_replace(jap:str, replacement:str) -> int:
        
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
        _jap_replace_count = 0

        _jap_lines = Kairyou.text_to_preprocess.split('\n')

        while (i < len(_jap_lines)):
            if (jap in _jap_lines[i]):

                _sentence = Kairyou._ner(_jap_lines[i]) # type:ignore

                for _entity in _sentence.ents:
                    if (_entity.text == jap and _entity.label_ == "PERSON"):
                        _jap_replace_count += 1
                        _jap_lines[i] = _jap_lines[i][:_entity.start_char] + \
                            replacement + _jap_lines[i][_entity.end_char:]

            i += 1

        Kairyou.text_to_preprocess = '\n'.join(_jap_lines)
        Kairyou._total_replacements += _jap_replace_count

        return _jap_replace_count

    @staticmethod
    def _add_missing_periods(text:str) -> str:
        """
        Adds closing periods before 」 where no punctuation is present.
        Must be called before any replacements occur.

        Parameters:
        text (str): The text to process

        Returns:
        str: The processed text with periods added where needed
        """
        pattern = r'([^。！？\.\!\?])」'
        return regex.sub(pattern, r'\1。」', text)