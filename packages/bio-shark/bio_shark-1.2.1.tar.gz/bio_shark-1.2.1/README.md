<h1 align="center">
<img src="https://git.mpi-cbg.de/tothpetroczylab/shark/-/raw/master/branding/logo/SharkDive_logo.png" width="300">
</h1><br>

# SHARK (Similarity/Homology Assessment by Relating K-mers)

To accurately assess homology between unalignable sequences, we developed an alignment-free sequence comparison algorithm, SHARK (Similarity/Homology Assessment by Relating K-mers). 

##  SHARK-dive 

We trained SHARK-dive, a machine learning homology classifier, which achieved superior performance to standard alignment in assessing homology in unalignable sequences, and correctly identified dissimilar IDRs capable of functional rescue in IDR-replacement experiments reported in the literature.

### 1. Dive-Score
Scoring the similarity between a pair of sequence

Variants:
   1. Normal (`SHARK-score (T)`)
   2. Sparse (`SHARK-score (best)`)

### 2. Dive-Predict
Find sequences similar to a given query from a target set   


## User Section

### Installation

SHARK officially supports Python versions >=3.9,<3.12.

**Recommended** Use within a local python virtual environment

```shell
python3 -m venv /path/to/new/virtual/environment
```

#### SHARK is installable from PyPI soon

```shell
$ pip install bio-shark
```

#### SHARK is also installable from source

* This allows users to import functionalities as a python package 
* This also allows user to run the functionalities as a command line utility 

```shell
$ git clone git@git.mpi-cbg.de:tothpetroczylab/shark.git
```
Once you have a copy of the source, you can embed it in your own Python package, or install it into your site-packages easily.

```shell
# Make sure you have the required Python version installed
$ python3 --version
Python 3.11.5

$ cd shark
$ python3 -m venv shark-env
$ source shark-env/bin/activate
$ (shark-env) % python -m pip install .
```

#### SHARK is also installable from GitLab source directly

```shell
$ pip install git+https://git.mpi-cbg.de/tothpetroczylab/shark.git
```

###  How to use?

### 1. Dive

#### 1.1. Scoring: Given two protein sequences and a k-mer length (1 to 20), score the similarity b/w them 

##### Inputs

1. Protein Sequence 1
2. Protein Sequence 2
3. Scoring-variant: Normal (`SHARK-score (T)`)/ Sparse (`SHARK-score (best)`)
   1. Threshold (for "Normal")
4. K-Mer Length (Should be <= smallest_len(sequences))

##### 1.1.1. As a command-line utility
* Run the command `shark-score`
* Enter sequences when command prompts
* Enter the variant (1/2) when the command prompts

```shell
% shark-score 
Enter Sequence 1:
> SSSSPINTHGVSTTVPSSNNTIIPSSDGVSLSQTDYFDTVHNRQSPSRRESPVTVFRQPSLSHSKSLHKDSKNKVPQISTNQSHPSAVSTANTPGPSPN
Enter Sequence 2:
> VAEREFNGRSNSLHANFTSPVPRTVLDHHRHELTFCNPNNTTGFKTITPSPPTQHQSILPTAVDNVPRSKSVSSLPVSGFPPLIVKQQQQQQLNSSSSASALPSIHSPLTNEH
Enter k-mer length (integer 1 - 10): > 5
Press: 1. Normal; 2. Sparse
> 1
Enter threshold:
>0.8
Similarity Score: 0.6552442773
```

##### 1.1.2. As an imported python package

```python
from bio_shark.core import utils
from bio_shark.dive.run import run_normal, run_sparse

dive_t_score = run_normal(
    sequence1="LASIDPTFKAN",
    sequence2="ERQKNGGKSDSDDDEPAAKKKVEYPIAAAPPMMMP",
    k=3,
    threshold=0.8
)   # Compute SHARK-score (T)  

dive_best_score = run_sparse(
    sequence1="LASIDPTFKAN",
    sequence2="ERQKNGGKSDSDDDEPAAKKKVEYPIAAAPPMMMP",
    k=3,
)   # Compute SHARK-score (best)
```

#### 1.2. Similarity Prediction

##### 1.2.1. As an imported python package

```python
from bio_shark.dive.prediction import Prediction

predictor = Prediction(q_sequence_id_map=<dict-fasta-id-seq>, t_sequence_id_map=<dict-fasta-id-seq>)

expected_out_keys = ['seq_id1', 'sequence1', 'seq_id2', 'sequence2', 'similarity_scores_k', 'pred_label', 'pred_proba']
output = predictor.predict()    # List of output objects; Each element is for one pair
```

##### 1.2.2. As a command-line utility
- Run the command `shark-dive` with the absolute path of the sequence fasta files as only argument
- Sequences should be of length > 10, since `prediction` is always based on scores of k = [1..10]
- _You may use the `sample_fasta_file.fasta` from `data` folder (Owncloud link)_


```shell
usage: shark-dive [-h] [--output_dir OUTPUT_DIR] query target

DIVE-Predict: Given some query sequences, compute their similarity from the list of target sequences;Target is
supposed to be major database of protein sequences

positional arguments:
  query       Absolute path to fasta file for the query set of input sequences
  target      Absolute path to fasta file for the target set of input sequences

options:
  -h, --help  show this help message and exit
  --output_dir OUTPUT_DIR
                        Output folder (default: current working directory)
  
$ shark-dive "<query-fasta-file>.fasta" "<target-fasta-file>.fasta"
Read fasta file from path <query-fasta-file>.fasta; Found 4 sequences; Skipped 0 sequences for having X
Read fasta file from path <target-fasta-file>.fasta; Found 6 sequences; Skipped 0 sequences for having X
Output stored at <OUTPUT_DIR>/<path-to-sequence-fasta-file>.fasta.csv
```

- Output CSV has the following column headers: 
    - (1) "Query": Fasta ID of sequence from Query list
    - (2) "Target": Fasta ID of sequence from Target list
    - (3..12) "SHARK-Score (k=*)": Similarity score between the two sequences for specific k-value
    - (13) "SHARK-Dive": Aggregated similarity score over all lengths of k-mer

## Publication
### SHARK enables homology assessment in unalignable and disordered sequences
`Chi Fung Willis Chow, Soumyadeep Ghosh, Anna Hadarovich, Agnes Toth-Petroczy*`

_Accepted_

Biorxiv link: https://www.biorxiv.org/content/10.1101/2023.06.26.546490v1

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

## Developer section

The following directory structure allows a developer to understand the codebase 

### Directory Structure
```
|-- src                # Package root
    |-- core                    # Core logic of sequence similarity matrix and common utilities
    |-- dive                    # Source code/logic functions related to "Dive"
|-- data                        # Local folder: Data directory
|-- tests                       # Unit tests
|-- requirements.txt            # Packages required for the project
|-- README.md

```

#### Simply run all unit-tests
1. Install test dependencies `pip install -r test-requirements.txt`
2. Run `python3 -m unittest`

Generate coverage:

```shell
$ coverage run -m unittest
$ coverage report 
```


#### Packaging and distribution

The project can be found here https://pypi.org/project/bio-shark/. An API token is required from PyPI to upload a distribution.

##### How to build the bio-shark package from the project root directory?

```shell
(packaging) $ python3 -m pip install --upgrade build
(packaging) $ python3 -m build

(packaging) $ ls -l dist 
bio-shark-1.0.0b1.tar.gz
bio-shark-1.0.0b1-py3-none-any.whl
```

### How to upload distribution files to PyPI?

Finally, we need to upload these files to PyPI using Twine. Use the following command from the project root
directory. Enter the PyPI credentials to complete uploading the package.

```shell
(packaging) $ python3 -m pip install --upgrade twine

# Run a check on the distribution files
(packaging) $ twine check dist/*

# Perform a test upload on testPyPI
(packaging) $ twine upload --repository testpypi dist/*

# Finally upload the distribution to PyPI
(packaging) $ twine upload dist/*
```
