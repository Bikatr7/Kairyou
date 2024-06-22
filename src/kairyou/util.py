## Copyright 2024 Kaden Bilyeu (Bikatr7) (https://github.com/Bikatr7) (https://github.com/Bikatr7/Kairyou)
## Use of this source code is governed by a GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import enum
import typing

## custom modules
from .exceptions import InvalidReplacementJsonKeys

##-------------------start-of-validate_replace_json()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _validate_replacement_json(replacement_json) -> typing.Tuple[typing.Literal["kudasai", "fukuin"], list]:

    """

    Validates the replacement json file.

    Parameters:
    replacement_json (dict) : The replacement json file.

    Returns:
    json_type (string) : The type of replacement json file. Either "kudasai" or "fukuin".
    replacement_rules (list) : The replacement rules for the replacement json file.

    Raises:
    InvalidReplacementJsonKeys : If the replacement json file is missing keys.

    """
    
    _kudasai_keys = ["kutouten", "unicode", "phrases", "single_words", "enhanced_check_whitelist", "full_names", "single_names", "name_like", "honorifics"]
    _fukuin_keys = ["specials", "basic", "names", "single-names", "full-names", "name-like", "honorifics"]

    try:
        if(all(_key in replacement_json for _key in _kudasai_keys)):
            return "kudasai", _kudasai_replacement_rules
        
        elif(all(_key in replacement_json for _key in _fukuin_keys)):
            return "fukuin", _fukuin_replacement_rules
        
        else:
            raise InvalidReplacementJsonKeys
        
    except AssertionError:
        raise InvalidReplacementJsonKeys

##-------------------start-of-_get_elapsed_time()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _get_elapsed_time(start:float, end:float) -> str:

    """

    Calculates elapsed time with an offset.

    Parameters:
    start (float) : Start time.
    end (float) : End time.

    Returns:
    _print_value (string): The elapsed time in a human-readable format.

    """

    _elapsed_time = end - start
    _print_value = ""

    if(_elapsed_time < 60.0):
        _print_value = str(round(_elapsed_time, 2)) + " seconds"
    elif(_elapsed_time < 3600.0):
        _print_value = str(round(_elapsed_time / 60, 2)) + " minutes"
    else:
        _print_value = str(round(_elapsed_time / 3600, 2)) + " hours"

    return _print_value

##-------------------start-of-Name---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Name(typing.NamedTuple):

    """
    
    Represents a Japanese name along with its equivalent english name.
    The Name class extends the NamedTuple class, allowing for the creation of a tuple with named fields.

    """

    jap : str
    eng : str

##-------------------start-of-ReplacementType---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ReplacementType(enum.Flag):

    """

    Represents how a name should be replaced when dealing with honorifics and overall replacements.

    The ReplacementType class extends the Flag class, allowing for the combination of name markers using bitwise operations.
    
    Name Markers:
    - NONE : No specific name marker.
    - FULL_NAME : Represents a full name, first and last name.
    - FIRST_NAME : Represents the first name only.
    - FULL_AND_FIRST : Represents both the full name and the first name separately.
    - LAST_NAME : Represents the last name only.
    - FULL_AND_LAST : Represents both the full name and the last name.
    - FIRST_AND_LAST : Represents both the first name and the last name.
    - ALL_NAMES : Represents all possible names.

    """

    NONE = 0 
    FULL_NAME = 1 
    FIRST_NAME = 2 
    FULL_AND_FIRST = 3 
    LAST_NAME = 4 
    FULL_AND_LAST = 5 
    FIRST_AND_LAST = 6 
    ALL_NAMES = 7

##-------------------start-of-vars---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_kudasai_replacement_rules = [
# (title, json_key, is_name, replace_name, honorific_type)
('Punctuation', 'kutouten', False, None, None),
('Unicode', 'unicode', False, None, None),
('Enhanced Check Whitelist', 'enhanced_check_whitelist',
    True, ReplacementType.ALL_NAMES, ReplacementType.ALL_NAMES),
('Full ReplacementType', 'full_names', True,
    ReplacementType.ALL_NAMES, ReplacementType.ALL_NAMES),
('Single ReplacementType', 'single_names', True,
    ReplacementType.ALL_NAMES, ReplacementType.ALL_NAMES),
('Name Like', 'name_like', True,
    ReplacementType.ALL_NAMES, ReplacementType.NONE),
('Phrases', 'phrases', False, None, None),
('Words', 'single_words', False, None, None),
]

_fukuin_replacement_rules = [
# title, json_key, is_name, replace_name, honorific_type
('Special', 'specials', False, None, None),
('Basic', 'basic', False, None, None),
('Imp ReplacementType', 'names', True, ReplacementType.ALL_NAMES, ReplacementType.ALL_NAMES),
('Remaining ReplacementType', 'full-names', True, ReplacementType.ALL_NAMES, ReplacementType.ALL_NAMES),
('Single ReplacementType', 'single-names', True, ReplacementType.LAST_NAME, ReplacementType.LAST_NAME),
('Name like', 'name-like', True, ReplacementType.LAST_NAME, ReplacementType.NONE),
]

_kudasai_blank_json={

    "honorifics": {

    },
  
    "single_words": {

    },
  
    "unicode": {

    },
  
    "phrases": {

    },
    
    "kutouten": {

    },
  
    "name_like": {
  
    },
  
    "single_names": {

    },
  
    "full_names": {

    },

    "enhanced_check_whitelist": {

    }
    
  }

_fukuin_blank_json={
  "specials": {

  },
  
  "basic": {

  },

  "names": {

  },

  "single-names": {

  },

  "full-names": {

  },

  "name-like": {

  },

  "honorifics": {

  }
}