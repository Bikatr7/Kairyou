## custom modules
from util import Name

##-------------------start-of-InvalidReplacementJsonName---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class InvalidReplacementJsonName(Exception):

    """

    Exception raised when the replacement json file is invalid.

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, name:Name):
        
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

    message = "Invalid replacement json file. Your json must contain the following keys: kutouten, unicode, phrases, single_words, enhanced_check_whitelist, full_names, single_names, name_like, and honorifics. Please see https://github.com/Bikatr7/Kairyou/tree/main/examples for an example replacement json file."
