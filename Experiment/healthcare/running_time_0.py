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

from Algorithm import ProvenanceSearch_10_20220421 as ps
from Algorithm import LatticeTraversal_2_2022405 as lt







data_file = r"../../InputData/Pipelines/healthcare/incomeK/before_selection_incomeK.csv"
selection_file = r"../../InputData/Pipelines/healthcare/incomeK/selection4.json"

print("========================== provenance search ===================================")
minimal_refinements1, minimal_added_refinements1, running_time1 = ps.FindMinimalRefinement(data_file, selection_file)

print("running time = {}".format(running_time1))

print("========================== lattice traversal ===================================")

minimal_refinements2, minimal_added_refinements2, running_time2 = lt.FindMinimalRefinement(data_file, selection_file)

print("running time = {}".format(running_time2))


print(*minimal_refinements1, sep="\n")


