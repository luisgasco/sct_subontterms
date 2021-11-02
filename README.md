# SCT_SubOntTerms 
A script to obtain a tsv file with child terms and codes of Snomed CT given a seed of codes 


<!-- GETTING STARTED -->
## Getting Started

This script has been developed with Python 3.6.9 in order to achieve compatibility with the rest of the TeMU tools.

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/luisgasco/sct_subontterms.git
   ```

2. Create a new virtual environment

   ```sh
   python3 -m venv .env
   ```

3. Activate the new environment

   ```sh
   source .env/bin/activate
   ```

4. Install the requirements

    ```sh
    pip install -r requirements.txt
    ```

## Usage

The sct_subontterms.py script has the following options:

* **Relationships file (-r or --rel_file)**: Path to the SnomedCT Relationship file in RF2 format. 
* **Concepts file (-c or --concept_file)**: Path to the SnomedCT Concept file in RF2 format
* **Output tsv (-o or --output_file)**: File in which you want to save the results (it can be a path/filename.tsv).
* **List of seed codes (-l or --code_list)**: List of codes separated by commas.
* **Root code to consider in SnomedCT (--root_code)**: Snomed concept id from which you want to generate the ontology file. For example if you want to consider only the branch "Pharmaceutical / biologic product" you should use the code "373873005", if you want to use the whole snomed ontology you should use the code "138875005".Defaults to "138875005"
* **Relationship types to consider in SnomedCT (--rel_types)**: Type of relationship to consider when building the ontology. Use string "116680003" if you only want to consider "Is a" relationships, use "all" if you want to consider all types of relationships (including concept model attributes).Defaults to "116680003"

Examples:
```bash
python sct_subontterms.py -r "/Path/to/Full/Terminoology/sct2_Relationship_Full_INT_20210731.txt" \
    -c "/Path/to/Full/Terminoology/sct2_Description_SpanishExtensionFull-es_INT_20210430.txt" \
    -o "output_terms.tsv" \
    -l 258695005,272103003,7389001
```