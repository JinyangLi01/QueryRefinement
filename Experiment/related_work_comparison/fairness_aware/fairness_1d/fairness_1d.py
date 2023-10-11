import copy
from typing import List, Any
import numpy as np
import pandas as pd
import time
from intbitset import intbitset
import json

from Algorithm import ProvenanceSearchValues_8_predicate_same_att_2 as ps
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
    result_output_file = r"./result_q" + str(q) + '_' + c + ".txt"
    result_output = open(result_output_file, "w")
    result_output.write("query {}, constraint {}\n".format(q, c))
    print("query", q)
    query_file = query_file_prefix + str(q) + ".json"
    with open(query_file) as f:
        query_info = json.load(f)

    print("========================== provenance search ===================================")
    minimal_refinements1, running_time1, assign_to_provenance_num, \
        provenance_time1, search_time1, time_first_minimal_refinement = \
        ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_format, time_limit)

    print(
        "running time = {}, num refinements = {}, time per refinement = {}, time first refinement = {}".format(
            running_time1,
            len(minimal_refinements1),
            running_time1 / len(minimal_refinements1),
            time_first_minimal_refinement,
        )
    )
    print(*minimal_refinements1, sep="\n")

    result_output.write(json.dumps(query_info))
    result_output.write("running time = {}, provenance time = {}, searching time = {}\n".format(
        running_time1, provenance_time1, search_time1))
    result_output.write("\n".join(str(item) for item in minimal_refinements1))


data_format = ".csv"
run('refine21', 2)
# run('refine31', 3)