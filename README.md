---------------------------------------------------------------------------------------------------------------------------------------------------
**Table of Contents**

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Kairyou](#kairyou)
  - [KatakanaUtil](#katakanautil)
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

Then, you can preprocess Japanese text by importing Kairyou and/or KatakanaUtil as follows:
```python
from kairyou import Kairyou, KatakanaUtil
```

Follow the usage examples provided in the [Usage](#usage) section for detailed instructions on preprocessing text and handling katakana.

---------------------------------------------------------------------------------------------------------------------------------------------------

**Installation**<a name="installation"></a>

Python 3.8 or higher, I haven't tested it on anything lower. 3.7 might work, but I'm not sure. Feedback is welcome.

Kairyou can be installed using pip:


```bash
pip install kairyou
```

This will install Kairyou along with its dependencies, including spaCy and a few other packages.

These are the dependencies that will be installed:
```
setuptools>=61.0

wheel

setuptools_scm>=6.0

tomli

spacy>=3.7.0,<3.8.0

ja_core_news_lg @ https://github.com/explosion/spacy-models/releases/download/ja_core_news_lg-3.7.0/ja_core_news_lg-3.7.0-py3-none-any.whl
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

Kairyou is mostly just preprocess(), but there are other functions available, however they are not intended for direct use. The preprocess() function takes in a string of Japanese text and a path to JSON file or dictionary of replacement rules. It returns the preprocessed text, a log of the replacements made, and a log of any errors that occurred during the preprocessing (typically none).

Currently, Kairyou supports two json types, "Kudasai" and "Fukuin". "Kudasai" is the native type and originated from that program, Fukuin is what the original onegai program used, as well as what the kroatoan's Fukuin program uses. No major differences in replacement are present between the two.

[Blank Kudasai Json](examples/blank_kudasai.json)

[Example Kudasai Json](examples/cote_kudasai.json)

[Blank Fukuin Json](examples/blank_fukuin.json)

[Example Fukuin Json](examples/cote_fukuin.json)

KatakanaUtil<a name="katakanautil"></a>

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

---------------------------------------------------------------------------------------------------------------------------------------------------

**License**<a name="license"></a>

This project (Kairyou) is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE.md) file for details.

The GPL is a copyleft license that promotes the principles of open-source software. It ensures that any derivative works based on this project must also be distributed under the same GPL license. This license grants you the freedom to use, modify, and distribute the software.

Please note that this information is a brief summary of the GPL. For a detailed understanding of your rights and obligations under this license, please refer to the [full license text](LICENSE.md).

---------------------------------------------------------------------------------------------------------------------------------------------------

**Contact**<a name="contact"></a>

If you have any questions or suggestions, feel free to reach out to me at [Tetralon07@gmail.com](mailto:Tetralon07@gmail.com).

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