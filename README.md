# The WHO's Director General's Speeches

Below can be found a list of data retrieval scripts that help make this work possible.
# Python

All scripts have been tested on Python 3.8.6.
The external modules that were used can be found in the `requirments.txt` file along with their versions.
**Note**: not all modules are required for all scripts.
If any of the modules are not already installed the normal `pip install -r requirments.txt` process should be followed.

## Scripts

Below is a brief summary of each of the scripts.
In order to fully regenerate the results, delete the cached folder and run the scripts in the order listed.
The pathing can be changed to any desired location.

1. [get_all_speeches.py](./get_all_speeches.py).
   This script will get the list of all of the director general's speeches from [here](https://www.who.int/director-general/speeches).
   The script can be run more than once.
   In this case the only new speeches will be retrieved.
   In the case of a network interruption causing a failed run, delete the full run and try again.
   ```{shell}
   python get_the_list_of_all_speeches.py -out d:/datasets/who
   ```
