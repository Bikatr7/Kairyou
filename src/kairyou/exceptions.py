## Copyright 2024 Kaden Bilyeu (Bikatr7) (https://github.com/Bikatr7) (https://github.com/Bikatr7/Kairyou)
## Use of this source code is governed by a GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

##-------------------start-of-KairyouException---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KairyouException(Exception):

    """
    
    Base exception class for Kairyou.
    

    """

##-------------------start-of-SpacyModelNotFound---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class SpacyModelNotFound(KairyouException):

    """

    Exception raised when the spacy model is not found.

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):
                
        message = f"Spacy model ja_core_news_lg not found. Please download the model using the following command: python -m spacy download ja_core_news_lg\n"
        
        super().__init__(message)

##-------------------start-of-InvalidReplacementJsonName---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class InvalidReplacementJsonName(KairyouException):

    """

    Exception raised when the replacement json file is invalid.

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        
        """
        
        Initializes the InvalidReplacementJsonName exception.

        """

        self.name = name
        
        message = f"Name lengths do not match for : {self.name.jap}/{self.name.eng}\nPlease correct Name discrepancy in JSON\n"
        
        super().__init__(message)
    

##-------------------start-of-InvalidReplacementJsonKeys---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class InvalidReplacementJsonKeys(KairyouException):

    """
    
    Exception raised when the replacement json keys are invalid.

    """

    message = """
    Invalid replacement json file. 
    Your json must contain the following keys for a kudasai json table : kutouten, unicode, phrases, single_words, enhanced_check_whitelist, full_names, single_names, name_like, and honorifics, or specials, basic, names, full-names, single-names, and name-like for a fukuin table.
    Please see https://github.com/Bikatr7/Kairyou/tree/main/examples for an example replacement json file."
    """

##-------------------start-of-InvalidReplacementJsonPath---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class InvalidReplacementJsonPath(KairyouException):

    """

    Exception raised when the replacement json path is invalid.

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, path:str):
        
        self.path = path

        message = f"Invalid path to replacement json file: {self.path}\nPlease check the path and try again\n"

        super().__init__(message)


class InvalidPreprocessingText(KairyouException):

    """

    Exception raised when the text to be preprocessed is invalid.

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, message:str):
        
        super().__init__(message)