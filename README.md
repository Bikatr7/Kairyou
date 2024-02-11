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

Pretty sure it requires 3.8 or higher, I haven't tested it on anything lower. 3.7 might work, but I'm not sure. Feedback is welcome.

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

Kairyou simplifies the preprocessing of Japanese text for NLP and NER tasks. Here's an example of how to use it:

```python
from kairyou import Kairyou

text = "Your Japanese text here."
replacement_json = "path/to/your/replacement_rules.json"  ## or a dict of rules
preprocessed_text, log, error_log = Kairyou.preprocess(text, replacement_json)

print(preprocessed_text)
```

Kairyou is mostly just preprocess() there are other functions available, but they are not intended for direct use. The preprocess() function takes in a string of Japanese text and a JSON file or dictionary of replacement rules. It returns the preprocessed text, a log of the replacements made, and a log of any errors that occurred during the preprocessing (typically none).

Note that rules must follow the format of the example JSON file [Blank Format JSON](examples/blank_replacements.json). You can also look at [COTE Replacements JSON](examples/cote_replacements.json) for an example of one that is filled out.

KatakanaUtil<a name="katakanautil"></a>

KatakanaUtil provides utility functions for handling katakana characters in Japanese text. Example usage:

```python
from kairyou import KatakanaUtil

katakana_word = "カタカナ"
if KatakanaUtil.is_katakana_only(katakana_word):
    print(f"{katakana_word} is composed only of Katakana characters.")
```

```
The following functions are available in KatakanaUtil:

is_katakana_only: Returns True if the input string is composed only of katakana characters.

is_actual_word: Returns True if the input string is a actual Japanese Katakana word (not just something made up or a name). List of words can be found [here](src/kairyou/lib/katakana_words.txt).

is_punctuation: Returns True if the input string is punctuation (Both Japanese and English punctuation are supported). List of punctuation can be found [here](src/kairyou/katakana_util.py).
```
---------------------------------------------------------------------------------------------------------------------------------------------------

**License**<a name="license"></a>

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE.md) file for details.

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

Kairyou was originally developed as a part of [Kudasai](https://github.com/Bikatr7/Kudasai), a Japanese preprocessor turned Machine Translator. It was later split off into its own package to be used independently of Kudasai for multiple reasons.

Kairyou gets its name from the Japanese word "Reform" (改良) which is pronounced "Kairyou". Which was chosen for two reasons, the first being that it was chosen during a large Kudasai rework, and the second being that it is a Japanese preprocessor, and the name "Reform" seemed fitting.

This package is also my first serious attempt at creating a Python package, so I'm sure there are some things that could be improved. Feedback is welcomed.