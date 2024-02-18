##-------------------start-of-InvalidReplacementJsonName---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class InvalidReplacementJsonName(Exception):

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

class InvalidReplacementJsonKeys(Exception):

    """
    
    Exception raised when the replacement json keys are invalid.

    """

    message = """
    Invalid replacement json file. 
    Your json must contain the following keys for a kudasai json table : kutouten, unicode, phrases, single_words, enhanced_check_whitelist, full_names, single_names, name_like, and honorifics, or specials, basic, names, full-names, single-names, and name-like for a fukuin table.
    Please see https://github.com/Bikatr7/Kairyou/tree/main/examples for an example replacement json file."
    """

##-------------------start-of-InvalidReplacementJsonPath---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class InvalidReplacementJsonPath(Exception):

    """

    Exception raised when the replacement json path is invalid.

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, path:str):
        
        self.path = path

        message = f"Invalid path to replacement json file: {self.path}\nPlease check the path and try again\n"

        super().__init__(message)

