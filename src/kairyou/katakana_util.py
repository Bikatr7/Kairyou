## built-in libraries
import string
import typing

## custom modules
from .util import Name
from .words import katakana_words as words

##--------------------start-of-KatakanaUtil------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KatakanaUtil:

    """
    
    Contains helper functions for katakana handling.

    """

    katakana_words = words.split("\n")

    ## https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
    KATAKANA_CHARSET = {
    '゠','ァ','ア','ィ','イ','ゥ','ウ','ェ','エ','ォ','オ','カ','ガ','キ','ギ','ク',
    'グ','ケ','ゲ','コ','ゴ','サ','ザ','シ','ジ','ス','ズ','セ','ゼ','ソ','ゾ','タ',
    'ダ','チ','ヂ','ッ','ツ','ヅ','テ','デ','ト','ド','ナ','ニ','ヌ','ネ','ノ','ハ',
    'バ','パ','ヒ','ビ','ピ','フ','ブ','プ','ヘ','ベ','ペ','ホ','ボ','ポ','マ','ミ',
    'ム','メ','モ','ャ','ヤ','ュ','ユ','ョ','ヨ','ラ','リ','ル','レ','ロ','ヮ','ワ',
    'ヰ','ヱ','ヲ','ン','ヴ','ヵ','ヶ','ヷ','ヸ','ヹ','ヺ','・','ー','ヽ','ヾ'
    }

    ## Punctuation unicode ranges:
    ## https://kairozu.github.io/updates/cleaning-jp-text
    PUNCTUATION_CHARSET = {
    '　','、','。','〃','〄','々','〆','〇','〈','〉','《','》','「','」','『','』',
    '【','】','〒','〓','〔','〕','〖','〗','〘','〙','〚','〛','〜','〝','〞','〟',
    '〠','〡','〢','〣','〤','〥','〦','〧','〨','〩','〪','〫','〬','〭','〮','〯',
    '〰','〱','〲','〳','〴','〵','〶','〷','〸','〹','〺','〻','〼','〽','〾','〿',
    '！','＂','＃','＄','％','＆','＇','（','）','＊','＋','，','－','．','／','：',
    '；','＜','＝','＞','？','［','＼','］','＾','＿','｀','｛','｜','｝','～','｟',
    '｠','｡','｢','｣','､','･','ー','※',' ',' ',' ',' ',"«", "»","_",
    ' ',' ',' ',' ',' ',' ',' ',
    '​','‌','‍','‎','‏','‐','‑','‒','–','—',
    '―','‖','‗','‘','’','‚','‛','“','”','„','‟','†','‡','•','‣','․','‥','…','‧',
    ' ',' ','‪','‫','‬','‭','‮',
    ' ','‰','‱','′','″','‴','‵','‶','‷','‸','‹','›','※','‼','‽','‾','‿',
    '⁀','⁁','⁂','⁃','⁄','⁅','⁆','⁇','⁈','⁉','⁊','⁋','⁌','⁍','⁎','⁏','⁐','⁑','⁒',
    '⁓','⁔','⁕','⁖','⁗','⁘','⁙','⁚','⁛','⁜','⁝','⁞',' ','⁠',
    '⁦','⁧','⁨','⁩','«','»','×',"△","▼"
    } | set(string.punctuation) ## EN punctuation set

##--------------------start-of-is_katakana_only()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_katakana_only(string:str) -> bool:

        """

        Checks if the string is only katakana.
        
        Parameters:
        string (str) : the string to check.

        Returns:
        bool : True if the word is only katakana, False otherwise.

        """

        return all([char in KatakanaUtil.KATAKANA_CHARSET for char in string])

##--------------------start-of-get_katakana_entities()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_katakana_entities(names:dict) -> typing.List[Name]:

        """

        Gets the katakana entities from the names dictionary.

        Returns:
        list (object - Name) : a list of Name objects.

        """

        return [Name(jap=j, eng=e) for e, j in names.items() if KatakanaUtil.is_katakana_only(j)]
    
##--------------------start-of-is_actual_word()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_actual_word(jap:str) -> bool:

        """
        
        Checks if the given japanese is an actual katakana word.

        Parameters:
        jap (str) : the katakana word to check.
 
        Returns:
        bool : True if the word is an actual katakana word, False otherwise.

        """

        if(jap in KatakanaUtil.katakana_words):
            return True
        
        else:
            return False
        
##--------------------start-of-is_punctuation()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_punctuation(string:str):

        """
        
        Checks if the given string is all punctuation.

        Parameters:
        string (str) : the string to check.

        Returns:
        bool : True if the word is all punctuation, False otherwise.

        """

        return all([char in KatakanaUtil.PUNCTUATION_CHARSET for char in string])