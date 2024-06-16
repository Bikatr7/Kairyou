---------------------------------------------------------------------------------------------------------------------------------------------------
**Table of Contents**

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Kairyou](#kairyou)
  - [KatakanaUtil](#katakanautil)
  - [Indexer](#indexer)
- [License](#license)
- [Contact](#contact)
- [Contribution](#contribution)
- [Notes](#notes)
- [Inspirations](#inspirations)

---------------------------------------------------------------------------------------------------------------------------------------------------

## Kairyou

Quickly preprocesses Japanese text using NLP/NER from SpaCy for Japanese translation or other NLP tasks. 

---------------------------------------------------------------------------------------------------------------------------------------------------
**Quick Start**<a name="quick-start"></a>

To get started with Kairyou, install the package via pip:

```bash
pip install kairyou
```

You must also install the jp_core_news_lg model from spaCy. This can be done by running the following command:

for windows:

```bash
python -m spacy download ja_core_news_lg
```

for linux:

```bash
python3 -m spacy download ja_core_news_lg
```

Then, you can preprocess Japanese text by importing Kairyou and/or KatakanaUtil/Indexer:
```python
from kairyou import Kairyou, KatakanaUtil, Indexer
```

Follow the usage examples provided in the [Usage](#usage) section for detailed instructions on preprocessing text and handling katakana.

---------------------------------------------------------------------------------------------------------------------------------------------------

**Installation**<a name="installation"></a>

Python 3.10+

Kairyou can be installed using pip:


```bash
pip install kairyou
```

This will install Kairyou along with its dependencies, including spaCy and a few other packages.

These are the dependencies/requirements that will be installed:
```
setuptools>=61.0

wheel

setuptools_scm>=6.0

tomli

spacy==3.7.5

regex>=2023.3.23

```
---------------------------------------------------------------------------------------------------------------------------------------------------

**Usage**<a name="usage"></a>

---------------------------------------------------------------------------------------------------------------------------------------------------

**Kairyou**<a name="kairyou"></a>

Kairyou is the global preprocessor client. Here's an example of how to use it:

```python
from kairyou import Kairyou

text = "Your Japanese text here."
replacement_json = "path/to/your/replacement_rules.json"  ## or a dict of rules
preprocessed_text, preprocessing_log, error_log = Kairyou.preprocess(text, replacement_json)

print(preprocessed_text)
```

Currently, Kairyou supports two json types, "Kudasai" and "Fukuin". "Kudasai" is the native type and originated from that program, Fukuin is what the original onegai program used, as well as what the kroatoan's Fukuin program uses. No major differences in replacement are present between the two.

Kairyou performs some post-processing on the text to correct any issues that may have arisen during the preprocessing.

[Blank Kudasai Json](examples/blank_kudasai.json)

[Example Kudasai Json](examples/cote_kudasai.json)

[Blank Fukuin Json](examples/blank_fukuin.json)

[Example Fukuin Json](examples/cote_fukuin.json)

---------------------------------------------------------------------------------------------------------------------------------------------------

**KatakanaUtil**<a name="katakanautil"></a>

KatakanaUtil provides utility functions for handling katakana characters in Japanese text. Example usage:

```python
from kairyou import KatakanaUtil

katakana_word = "カタカナ"
if KatakanaUtil.is_katakana_only(katakana_word):
    print(f"{katakana_word} is composed only of Katakana characters.")
```

The following functions are available in KatakanaUtil:

is_katakana_only: Returns True if the input string is composed only of katakana characters.

is_actual_word: Returns True if the input string is a actual Japanese Katakana word (not just something made up or a name). List of words can be found [here](src/kairyou/words.py).

is_punctuation: Returns True if the input string is punctuation (Both Japanese and English punctuation are supported). List of punctuation can be found [here](src/kairyou/katakana_util.py).

is_repeating_sequence: Returns True if the input string is just a repeating sequence of characters. (e.g. "ジロジロ")

is_more_punctuation_than_japanese: Returns True if the input string has more punctuation than Japanese characters.

is_partially_english: Returns True if the input string has any English characters in it.

---------------------------------------------------------------------------------------------------------------------------------------------------

**Indexer**<a name="indexer"></a>

Indexer is for "indexing" Japanese text. What this means is that, given input_text, a knowledge_base, and a replacements_json. It will return a list of new "names", and the occurrence which was flagged.

What is considered a name is a bit complicated. But:
1. Must have the "person" label when using spaCy's NER.
2. Cannot have more punctuation than Japanese characters.
3. Cannot be a repeating sequence of characters.
4. Cannot be an actual Japanese Katakana word.
5. Cannot have any english characters in it. (Names that are pre-replaced would have already been in the other texts, plus the JP NER model seems to have trouble with ENG in general)

So, it'll return names that don't in the other texts.

This can be done via index()
```py
from kairyou import Indexer

input_text = "Your Japanese text here." ## or a path to a text file
knowledge_base = ["more Japanese text here.", "even_more_japanese_text_here"] ## or a path to a text file or directory full of text files
replacements_json = "path/to/your/replacement_rules.json"  ## or a dict of rules

## You can optionally send a list of strings to ignore, but this is not required.

NamesAndOccurrences, indexing_log = Indexer.index(input_text, knowledge_base, replacements_json) ## also takes in a list of strings to ignore, defaults to []
```

NamesAndOccurrences is a list of named tuples, with the following fields:
1. name: The name that was found.
2. occurrence: The occurrence of the name in the input_text.

Indexing_log is a string of the log of the indexing process. What was indexed, it's occurrence, what was ignored, and time elapsed.

Index works with both Fukuin and Kudasai jsons.

---------------------------------------------------------------------------------------------------------------------------------------------------

**License**<a name="license"></a>

This project, Kairyou, is licensed under the GNU Lesser General Public License v2.1 (LGPLv2.1) - see the LICENSE file for complete details.

The LGPL is a permissive copyleft license that enables this software to be freely used, modified, and distributed. It is particularly designed for libraries, allowing them to be included in both open source and proprietary software. When using or modifying Kairyou, you can choose to release your work under the LGPLv2.1 to contribute back to the community or incorporate it into proprietary software as per the license's permissions.

Under the LGPLv2.1, any modifications made to Kairyou's libraries must be shared under the same license, ensuring the open source nature of the library itself is maintained. However, it allows the wider work that includes the library to remain under different licensing terms, provided the terms of the LGPLv2.1 are met for the library.

I encourage the use of Kairyou within all projects. This approach ensures a balance between open collaboration and the flexibility required for proprietary development.

For a thorough explanation of the conditions and how they may apply to your use of the project, please review the full license text. This comprehensive documentation will offer guidance on your rights and obligations when utilizing LGPLv2.1 licensed software.

---------------------------------------------------------------------------------------------------------------------------------------------------

**Contact**<a name="contact"></a>

If you have any questions or suggestions, feel free to reach out to me at [Bikatr7@proton.me](mailto:Bikatr7@proton.me)

Also feel free to check out the [GitHub repository](https://github.com/Bikatr7/Kairyou) for this project.

Or the issue tracker [here](https://github.com/Bikatr7/Kairyou/issues).

---------------------------------------------------------------------------------------------------------------------------------------------------

**Contribution**<a name="contribution"></a>

Contributions are welcome! I don't have a specific format for contributions, but please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

---------------------------------------------------------------------------------------------------------------------------------------------------

**Notes**<a name="notes"></a>

Kairyou was originally developed as a part of [Kudasai](https://github.com/Bikatr7/Kudasai), a Japanese preprocessor later turned Machine Translator. It was later split off into its own package to be used independently of Kudasai for multiple reasons.

Kairyou gets its name from the Japanese word "Reform" (改良) which is pronounced "Kairyou". Which was chosen for two reasons, the first being that it was chosen during a large Kudasai rework, and the second being that it is a Japanese preprocessor, and the name seemed fitting.

This package is also my first serious attempt at creating a Python package, so I'm sure there are some things that could be improved. Feedback is welcomed.

---------------------------------------------------------------------------------------------------------------------------------------------------

**Inspirations**<a name="inspirations"></a>

Kudasai and by extension Kairyou was originally derived from [Void's Script](https://github.com/Atreyagaurav/mtl-related-scripts) later [Onegai](https://github.com/Atreyagaurav/onegai)

Kairyou also took some inspiration from [Fukuin](https://github.com/kroatoanjp/nlp-mtl-preprocessing-script) and it's approach with Katakana.

Thanks to all of the above for the inspiration and the work they put into their projects.
