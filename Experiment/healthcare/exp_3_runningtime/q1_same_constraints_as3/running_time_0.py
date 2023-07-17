"""
executable
without optimizations
"""

import copy
from typing import List, Any
import numpy as np
import pandas as pd
import time
from intbitset import intbitset
import json
import sys

sys.path.append('../../../../')
from Algorithm import ProvenanceSearchValues_8_20230119 as ps
from Algorithm import LatticeTraversal_5_20230121 as lt

data_file_prefix = r"../../../../InputData/Healthcare/incomeK/"
query_file_prefix = r"query"
constraint_file_prefix = r"constraint"
time_output_prefix = r"./result_"


def file(q, c):
    time_output_file = time_output_prefix + str(q) + str(c) + "1.csv"
    time_output = open(time_output_file, "w")
    time_output.write("selection file, running time ps, running time lt\n")
    return time_output

result_output_file = r"./running_time_result.txt"
result_output = open(result_output_file, "w")
result_output.write("selection file, result\n")


time_limit = 60 * 60 * 3
separator = ','

def compare(q, c, time_output):
    print("run with query{} constraint{}".format(q, c))
    result_output.write("query{} constraint{}\n".format(q, c))
    query_file = query_file_prefix + str(q) + ".json"
    constraint_file = constraint_file_prefix + str(c) + ".json"

    print("========================== provenance search ===================================")
    minimal_refinements1, _, running_time1, num_refinements1, \
    provenance_time1, search_time1 = \
        ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_file_format, time_limit)

    print("running time = {}, num_refinements1 = {}".format(running_time1, num_refinements1))
    print(*minimal_refinements1, sep="\n")

    running_time2, provenance_time2, search_time2 = 0, 0, 0
    print("========================== lattice traversal ===================================")

    minimal_refinements2, minimal_added_refinements2, running_time2, num_refinements2, provenance_time2, search_time2 = \
        lt.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_file_format, time_limit)
    if running_time2 > time_limit:
        print("naive alg out of time")
    else:
        print("running time = {}, num_refinements2 = {}".format(running_time2, num_refinements2))
        print(*minimal_refinements2, sep="\n")

    time_output.write("\n")
    idx = "Q" + str(q) + "C" + str(c)
    time_output.write("{},{:0.2f},{:0.2f},{:0.2f},{}\n".format(idx, running_time1, provenance_time1,
                                                            search_time1, num_refinements1))
    if running_time2 < time_limit:
        time_output.write("{},{:0.2f},{:0.2f},{:0.2f},{}"
                          "{:0.2f},{:0.2f},{:0.2f},{}\n".format(idx, running_time1, provenance_time1, search_time1,
                                                                num_refinements1,
                                                             running_time2, provenance_time2, search_time2, num_refinements2))
    else:
        time_output.write("{},{:0.2f},{:0.2f},{:0.2f},{},,,\n".format(idx, running_time1, provenance_time1,
                                                                   search_time1, num_refinements1))
    result_output.write("{}\n".format(idx))
    result_output.write(",".join(str(item) for item in minimal_refinements1))
    result_output.write("\n")
    result_output.write("\n".join(str(item) for item in minimal_refinements1))
    result_output.write("\n")


summary_file = open(r"time1.csv", "w")
summary_file.write("file,PS,LT\n")

data_file_format = '.csv'

def run(q, c):
    time_output = file(q, c)
    compare(q, c, time_output)
    time_output.close()


# run(1, 1)
# run(1, 2)
run(1, 3)
# run(2, 1)
# run(2, 2)
# run(2, 3)
