## Copyright 2024 Kaden Bilyeu (Bikatr7) (https://github.com/Bikatr7) (https://github.com/Bikatr7/Kairyou)
## Use of this source code is governed by a GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import string
import typing

## custom modules
from .util import Name
from .words import _katakana_words as _words

##--------------------start-of-KatakanaUtil------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KatakanaUtil:

    """
    
    Contains helper functions for katakana handling.

    """

    katakana_words = _words.split("\n")

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

        return all([_char in KatakanaUtil.KATAKANA_CHARSET for _char in string])

##--------------------start-of-_get_katakana_entities()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _get_katakana_entities(names:dict) -> typing.List[Name]:

        """

        Gets the katakana entities from the names dictionary.

        Returns:
        list (object - Name) : a list of Name objects.

        """

        return [Name(jap=_j, eng=_e) for _e, _j in names.items() if KatakanaUtil.is_katakana_only(_j)]
    
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

        return jap in KatakanaUtil.katakana_words
        
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

##--------------------start-of-is_repeating_sequence()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
    @staticmethod
    def is_repeating_sequence(word:str) -> bool:

        """

        Checks if the given word has a repeating sequence.

        Parameters:
        word (str) : the word to check.

        Returns:
        bool : True if the word has a repeating sequence, False otherwise.

        """

        for i in range(1, len(word)//2 + 1):  # Only need to iterate to half the word length
            ## Check every possible subsequence size
            for ii in range(len(word) - i):
                if word[ii:ii+i] == word[ii+i:ii+2*i]:
                    return True
                
        return False
    
##--------------------start-of-more_punctuation_than_japanese()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_more_punctuation_than_japanese(text:str) -> bool:

        """

        Checks if the given text has more punctuation than Japanese characters.

        Parameters:
        text (str) : the text to check.

        Returns:
        bool : True if the text has more punctuation than Japanese characters, False otherwise.

        """

        ## Count non-punctuation (assumed to be Japanese) and punctuation characters
        _non_punctuation_count = sum(1 for _char in text if _char not in KatakanaUtil.PUNCTUATION_CHARSET)
        _punctuation_count = sum(1 for _char in text if _char in KatakanaUtil.PUNCTUATION_CHARSET)
        
        return _punctuation_count > _non_punctuation_count
    
##--------------------start-of-is_partially_english()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def is_partially_english(text:str) -> bool:
        
        """
        
        Checks if the given text is partially English.
        
        Parameters:
        text (str) : the text to check.
        
        Returns:
        bool : True if the text is partially English, False otherwise.
        
        """
        
        return any([_char in string.ascii_letters for _char in text])