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

from Algorithm import ProvenanceSearchValues_4_20220712 as ps
from Algorithm import LatticeTraversal_2_2022405 as lt


minimal_refinements1 = []
minimal_added_refinements1 = []
running_time1 = []

minimal_refinements2 = []
minimal_added_refinements2 = []
running_time2 = []


data_file = r"../../../InputData/Adult/adult.data"
query_file_prefix = r"./query"


def run_constraint(c):
    print("running adult query change constraint {}".format(c))
    constraint_file = r"./constraint" + str(c) + ".json"


    time_output_file = r"./query_change_" + str(c) + ".csv"
    time_output = open(time_output_file, "w")
    time_output.write("income,PS,LT\n")

    result_output_file = r"./result_" + str(c) + ".txt"
    result_output = open(result_output_file, "w")
    result_output.write("selection file, result\n")

    for i in range(1, 9):
        query_file = query_file_prefix + str(i) + ".json"
        print("========================== provenance search ===================================")
        minimal_refinements1, running_time1 = \
            ps.FindMinimalRefinement(data_file, query_file, constraint_file)
        print("running time = {}".format(running_time1))

        print("========================== lattice traversal ===================================")
        minimal_refinements2, minimal_added_refinements2, running_time2 = \
            lt.FindMinimalRefinement(data_file, query_file, constraint_file)
        print("running time = {}".format(running_time2))
        print(*minimal_refinements1, sep="\n")
        result_output.write("\n")
        idx = i * 50
        time_output.write("{}, {:0.2f}, {:0.2f}\n".format(idx, running_time1, running_time2))
        result_output.write("{}\n".format(idx))
        result_output.write(", ".join(str(item) for item in minimal_added_refinements1))
        result_output.write("\n")
        result_output.write("\n".join(str(item) for item in minimal_refinements1))
        result_output.write("\n")
    result_output.close()
    time_output.close()

run_constraint(1)