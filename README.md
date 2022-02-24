# The WHO's Director General's Speeches

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4391412.svg)](https://doi.org/10.5281/zenodo.4391412)

Below is the Gen 2 service for retrieving the WHO's Director General's Speeches.

# Operation

## Install

You can install the package using the following steps:

1. `pip` install using an _admin_ prompt
   ```{ps1}
   pip uninstall WHOSpeeches
   pip install -v git+https://github.com/WHOSpeechAnalysis/data.git
   ```

## Run

You can run the package in the following ways:

1. Get all the WHO's Director General's Speeches as a single csv from scratch.
   ```{ps1}
   WHOSpeeches -out "c:/data/who/speeches.csv"
   ```

## Scripts

Below is a brief summary of each of the scripts.
In order to fully regenerate the results, delete the cached folder and run the scripts in the order listed.
The pathing can be changed to any desired location.

1. Open a PowerShell window and change to the `~/code` folder.
   ```{ps1}
   cd "D:\repos\WHOSpeechAnalysis\data\code"
   ```
2. [get_speeches_list](./code/get_speeches_list.py).
   This script will get the list of all of the director general's speeches from [here](https://www.who.int/director-general/speeches).
   The script can be run more than once.
   In this case the only new speeches will be retrieved.
   In the case of a network interruption causing a failed run, delete the full run and try again.
   ```{ps1}
   python get_speeches_list.py -out d:/datasets/who/raw
   ```
3. [convert_speeches_list](./code/convert_speeches_list.py).
   This script will convert the raw HTML list of links to the director general's speeches to text.
   The script can be run more than once.
   In this case the file is completely regenerated.
   ```{ps1}
   python convert_speeches_list.py -in d:/datasets/who/raw -out d:/datasets/who/speeches.txt
   ```
4. [get_speeches_text](./code/get_speeches_text.py).
   This script will get the HTML of all of the director general's speeches
   The script can be run more than once.
   In this case the only new speeches that were not previously downloaded will be retrieved.
   ```{ps1}
   python get_speeches_text.py -in d:/datasets/who/speeches.txt -out d:/datasets/who/raw
   ```
5. [convert_speeches_text](./code/convert_speeches_text.py).
   This script will convert the raw HTML speech of the director general's speeches to text.
   The script can be run more than once.
   In this case the file is completely regenerated.
   ```{ps1}
   python convert_speeches_text.py -in d:/datasets/who/raw -out d:/datasets/who/corpus.jsonl
   ```
6. [qa_speeches_text](./code/qa_speeches_text.py).
   This script runs a simple QA check on the data.
   The script can be run more than once.
   ```{ps1}
   python qa_speeches_text.py -raw d:/datasets/who/raw -jsonl d:/datasets/who/corpus.jsonl -out d:/datasets/who/qa.csv
   ```
7. [tokenize_speeches_text](./code/tokenize_speeches_text.py).
   This script will tokenize the raw speech text, converting one paragraph per line to one sentence per line.
   Additional cleanup (i.e. ` to ') will also be performed.
   The script can be run more than once.
   In this case the file is completely regenerated.
   ```{ps1}
   python tokenize_speeches_text.py -in d:/datasets/who/corpus.jsonl -out d:/datasets/who/corpus.tokenized.jsonl
   ```

# Development

## Prerequisites

You can install the package _for development_ using the following steps:

**Note**: You can replace steps 1-3 with a VSCode Git:Clone

1. Download the project from [GitHub](https://github.com/WHOSpeechAnalysis/data)
   * Click the green "Code" button on the right.
     Select "Download Zip"
2. Remove zip protections by right-clicking on the file, selecting properties, and checking "security: unblock"
3. Unzip the folder.
   I recommend using the folder _c:/repos/WHOSpeechAnalysis/data_
4. Run `pip`'s edit install using an _admin_ prompt
   ```{ps1}   
   pip uninstall WHOSpeeches
   pip install -v -e c:/repos/WHOSpeechAnalysis/data
   ```
5. Install the `nltk` add-ons using an _admin_ prompt
   ```{ps1}   
   python -c "import nltk;nltk.download('punkt')"
   ```
