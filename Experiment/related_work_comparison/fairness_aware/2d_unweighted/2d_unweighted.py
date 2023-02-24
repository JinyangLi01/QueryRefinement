import copy
from typing import List, Any
import numpy as np
import pandas as pd
import time
from intbitset import intbitset
import json

from Algorithm import ProvenanceSearchValues_8_20230119 as ps
from Algorithm import LatticeTraversal_5_20230121 as lt


minimal_refinements1 = []
minimal_added_refinements1 = []
running_time1 = []

minimal_refinements2 = []
minimal_added_refinements2 = []
running_time2 = []


data_file_prefix = r"../../../../../InputData/TPC-H/100Mdata/"
query_file_prefix = r"./q3_"
constraint_file_prefix = r"../"
time_limit = 5 * 60
separator = ' '

time_output_prefix = r"./result_"


constraint_file = r"./constraint_" + c + ".json"

time_output_file = r"./query_change_q3_" + c + ".csv"
time_output = open(time_output_file, "w")
time_output.write("_,PS,PS_prov,PS_search,base,base_prov,base_search\n")

result_output_file = r"./result_query_change_q3" + c + ".txt"
result_output = open(result_output_file, "w")
result_output.write("selection file, result\n")

print("query", i)
query_file = query_file_prefix + str(i) + ".json"
print("========================== provenance search ===================================")
minimal_refinements1, running_time1, _, \
    provenance_time1, search_time1 = \
    ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, time_limit)

print("running time = {}".format(running_time1))
print(*minimal_refinements1, sep="\n")