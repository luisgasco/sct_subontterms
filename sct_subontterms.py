#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: luisgasco
Script to generate a terminology tsv file with concepts of SnomedCT given a list of seed codes.
You will get the concept
 to normaliza clinical entities to controlled vocabularies

"""
import sys
import pandas as pd
import networkx as nx
import numpy as np
from optparse import OptionParser

def get_sucessors(g, code):
    """Get sucessors of a given code in a the given ontology g

    Args:
        g (Networkx DiGraph): Working ontology in Digraph format
        code (str): Code in str format

    Returns:
        lst: List of strings of the successors of "code"
    """
    return [key for key in g.successors(code)]

def get_rec(g,lista,recursive_list):
    """Recursive function to get sucessors of a givel list of codes in a given ontology "g".

    Args:
        g (Networkx DiGraph): Working ontology in Digraph format
        lista (lst): List os strings representing the codes to get sucessors.
        recursive_list (lst): List to save sucessors in the recursive function

    Returns:
        lst: List of strings of the successors of "code"
    """
    for a in lista:
        sucessors=get_sucessors(g,a)
        recursive_list.extend(sucessors)
        get_rec(g, sucessors,recursive_list)
    return recursive_list


def load_ontology(file_name_rel, root_concept_code="138875005", relation_types = "116680003"):
    """Function to load SnomecCT relationships from RF2 format to netowrkx model.
    Args:
        file_name_rel (str): Path to the SnomedCT Relationship file in RF2 format
        root_concept_code (str, optional): snomed code of the code from which you want to generate
                                           the ontology file (For example if we want the branch
                                           "Pharmaceutical / biologic product" we would use the code
                                           "373873005", if we want the whole snomed ontology we would
                                           use the code "138875005").Defaults to "138875005".
        relation_types (str, optional): Type of relationship to consider when building the ontology.
                                        Use string "116680003" if you only want to consider "Is a"
                                        relationships, use "all" if you want to consider all types
                                        of relationships (including concept model attributes).Defaults to "116680003".

    Returns:
        Networkx DiGraph: SnomedCT model in a NetworkxDigraph format.
    
    This code is based on the one written by @emreg00 (https://github.com/emreg00/toolbox/blob/master/parse_snomedct.py)
    """
    ontology = nx.DiGraph()
    f = open(file_name_rel)
    header = f.readline().strip("\n")
    col_to_idx = dict((val.lower(), i) for i, val in enumerate(header.split("\t")))
    for line in f:
        words = line.strip("\n").split("\t")
        if relation_types == "116680003": #"Is a" relationship code
            if words[col_to_idx["typeid"]] in relation_types:
                source_id = words[col_to_idx["sourceid"]]
                target_id = words[col_to_idx["destinationid"]]
                ontology.add_edge(target_id, source_id)
        else: # All
            source_id = words[col_to_idx["sourceid"]]
            target_id = words[col_to_idx["destinationid"]]
            ontology.add_edge(target_id, source_id)
    ontology = nx.dfs_tree(ontology, root_concept_code)
    return ontology

# Function to parse comma-´separated values
def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))



def main(argv=None):
    parser = OptionParser()
    parser.add_option("-r", "--rel_file", dest="rel_file",
                    help="Path to the SnomedCT Relationship file in RF2 format")
    parser.add_option("-c", "--concept_file", dest = "concept_file", help = "")
    parser.add_option("-o", "--output_file", dest="output_file", help="")
    parser.add_option("-l", "--code_list", dest = "code_list", type=str, action="callback", callback=get_comma_separated_args, help="Codes to get ")
    parser.add_option("--root_code", dest = "root_code", default = "138875005", type=str,help="")
    parser.add_option("--rel_types", dest = "rel_types", default = "all", type=str,help="")
    (options, args) = parser.parse_args(argv)


    # Variables to be used
    relationship_file = options.rel_file
    concepts_file = options.concept_file
    output_terminology = options.output_file
    code_list = options.code_list

    # Get ontology data:
    print("Loading SnomedCT into a DiGraph Networkx object...")
    g = load_ontology(relationship_file, root_concept_code = options.root_code, relation_types=options.rel_types)
    print("Object loaded")


    # Get sucessors from original codes
    print("You are going to get the SnomedCT branches of the codes {}".format(code_list))
    recursive_list = list()
    lista_end = get_rec(g,code_list,recursive_list)  
    lista_end_int = [int(key) for key in lista_end]

    # Load concepts
    concepts_df = pd.read_csv(concepts_file, sep="\t")

    # Filter concepts with sucessors found:
    concepts_df_filt = concepts_df[concepts_df.conceptId.isin(lista_end_int)]

    # Save data into output file as a term file.
    concepts_df_filt[["conceptId","term"]].to_csv(output_terminology, index = False, sep="\t", header = False)
    
if __name__ == "__main__":
  sys.exit(main())