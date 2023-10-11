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

minimal_refinements1 = []
minimal_added_refinements1 = []
running_time1 = []

minimal_refinements2 = []
minimal_added_refinements2 = []
running_time2 = []


def JacardSimilarity(set1, set2):
    return len(set1 & set2) / len(set1 | set2)


data_file_prefix = r"../../data/"
query_file_prefix = r"./q"
constraint_file_prefix = r"./"
time_limit = 60 * 30
separator = ' '
time_output_prefix = r"./result_"


def run_constraint(q):
    print("running query {}".format(q))

    query_file = query_file_prefix + str(q) + ".json"

    time_output_file = r"./constraint_change_q" + str(q) + ".csv"
    time_output = open(time_output_file, "w")
    # time_output.write("_,PS,PS_prov,PS_search,base,base_prov,base_search\n")

    result_output_file = r"./result_constraint_change_q" + str(q) + ".txt"
    result_output = open(result_output_file, "w")
    result_output.write("selection file, result\n")
    data_format = ".csv"
    single_binary_sensitive_att = True

    for i in [0, 1, 3, 5, 7, 9, 11]:
        print("\nconstraint {}\n".format(i))
        constraint_file = r"./constraint_refine" + str(i) + ".json"
        print("========================== provenance search ===================================")
        minimal_refinements1, order_in_results, running_time1, assign_to_provenance_num, \
            provenance_time1, search_time1, time_first_minimal_refinement = \
            ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_format,
                                     single_binary_sensitive_att, time_limit)

        print("running time = {}, num refinements = {}, "
              "time per refinement = {}, time_first_minimal_refinement = {}".
              format(running_time1, len(minimal_refinements1),
                     running_time1 / len(minimal_refinements1), time_first_minimal_refinement))

        print(*minimal_refinements1, sep="\n")

        result_output.write("\n")
        idx = i
        time_output.write(
            "{},{},{:.3f},{:0.3f},{:.3f}\n".format(idx, len(minimal_refinements1), running_time1,
                                                   running_time1 / len(minimal_refinements1),
                                                   time_first_minimal_refinement))
        result_output.write("{}\n".format(idx))
        result_output.write(",".join(str(item) for item in minimal_added_refinements1))
        result_output.write("\n")
        result_output.write("\n".join(str(item) for item in minimal_refinements1))
        result_output.write("\n")
    result_output.close()
    time_output.close()


run_constraint(1)
