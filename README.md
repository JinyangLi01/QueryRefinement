# Query Refinement for Diversity Constraint Satisfaction

Note: this is a private repo maintained for my own reference which contains all versions of code/experiments.
The public repo for the paper can be found at https://github.com/JinyangLi01/Query_refinement.


## Abstract
Diversity, group representation, and similar needs often apply to query results, which in turn require constraints on the sizes of various subgroups in the result set. Traditional relational queries only specify conditions as part of the query predicate(s) and do not support such restrictions on the output. In this paper, we study the problem of modifying queries to have the result satisfy constraints on the sizes of multiple subgroups in it. This problem, in the worst case, cannot be solved in polynomial time. Yet, with the help of provenance annotation, we are able to develop a query refinement method that works quite efficiently, as we demonstrate through extensive experiments. 



## About this repo
### Algorithms
1. our solution: Algorithm/ProvenanceSearchValues_6_20220825
2. naive solution lattice traversal: Algorithm/LatticeTraversal_4_20220901

### Experiments
In Experiments folder, with three datasets: adult, compas, healthcare



