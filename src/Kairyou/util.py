## built-in libraries
import enum
import typing

##-------------------start-of-get_elapsed_time()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_elapsed_time(start:float, end:float) -> str:

    """

    Calculates elapsed time with an offset.

    Parameters:
    start (float) : Start time.
    end (float) : End time.

    Returns:
    print_value (string): The elapsed time in a human-readable format.

    """

    elapsed_time = end - start
    print_value = ""

    if(elapsed_time < 60.0):
        print_value = str(round(elapsed_time, 2)) + " seconds"
    elif(elapsed_time < 3600.0):
        print_value = str(round(elapsed_time / 60, 2)) + " minutes"
    else:
        print_value = str(round(elapsed_time / 3600, 2)) + " hours"

    return print_value

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