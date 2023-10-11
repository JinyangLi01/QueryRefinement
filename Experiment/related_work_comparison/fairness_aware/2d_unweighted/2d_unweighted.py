import copy
from typing import List, Any
import numpy as np
import pandas as pd
import time
from intbitset import intbitset
import json

# from Algorithm import ProvenanceSearchValues_8_complex_constraints as ps
from Algorithm import ProvenanceSearchValues_8_complex_optimized_binary as ps
from Algorithm import LatticeTraversal_5_20230121 as lt


def JacardSimilarity(set1, set2):
    return len(set1 & set2) / len(set1 | set2)


data_file_prefix = r"../data/"
query_file_prefix = r"./q"
constraint_file_prefix = r"./"
time_limit = 60 * 30
separator = ' '

time_output_prefix = r"./result_"

def run(c, q):
    constraint_file = r"./constraint_" + c + ".json"

    time_output_file = r"./query_change_q1_" + c + ".csv"
    time_output = open(time_output_file, "w")
    time_output.write("_,PS,PS_prov,PS_search,base,base_prov,base_search\n")

    result_output_file = r"./result_query_change_q1" + c + ".txt"
    result_output = open(result_output_file, "w")
    result_output.write("selection file, result\n")

    data_format = ".csv"
    print("query", q)
    query_file = query_file_prefix + str(q) + ".json"
    single_binary_sensitive_att = True

    print("========================== provenance search ===================================")
    minimal_refinements1, order_in_results, running_time1, assign_to_provenance_num, \
        provenance_time1, search_time1, time_first_minimal_refinement = \
        ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_format,
                                 single_binary_sensitive_att, time_limit)

    print("running time = {}, num refinements = {}, time per refinement = {}, time first refinement = {}".
          format(running_time1, len(minimal_refinements1), running_time1 / len(minimal_refinements1),
                 time_first_minimal_refinement))
    print(*minimal_refinements1, sep="\n")


# run('refine11', 1)

run('refine21', 2)