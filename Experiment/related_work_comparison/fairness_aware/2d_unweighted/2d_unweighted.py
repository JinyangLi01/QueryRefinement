import copy
from typing import List, Any
import numpy as np
import pandas as pd
import time
from intbitset import intbitset
import json

from Algorithm import ProvenanceSearchValues_8_optimized as ps
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
    print("========================== provenance search ===================================")
    minimal_refinements1, running_time1, _, \
        provenance_time1, search_time1 = \
        ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_format, time_limit)

    print("running time = {}".format(running_time1))
    print(*minimal_refinements1, sep="\n")


run('refine11', 1)