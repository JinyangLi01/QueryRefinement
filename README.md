# QueryRefinement

## Abstract
It is a common need to have diversity and adequate group representation in a query result set, which requires constraints on the size of subgroups in the result set.
Traditional relational databases, however, generate results that satisfy constraints as part of the query.
In this paper, we study the problem of modifying queries to have the result satisfy constraints on the sizes of multiple subgroups in it.
This problem, in the worst case, cannot be solved in polynomial time.
Yet, with the help of provenance annotation, we are able to develop a query refinement method that works quite efficiently, as we demonstrate through extensive experiments. 

## About this repo
### Algorithms
1. our solution: Algorithm/ProvenanceSearchValues_6_20220825
2. naive solution lattice traversal: Algorithm/LatticeTraversal_4_20220901

### Experiments
In Experiments folder, with three datasets: adult, compas, healthcare
