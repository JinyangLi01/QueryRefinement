
# Sep. 1, 2021

1. understand the problem
2. without notion of Provenance, think of a naive solution, or prove it is NPhard
3. If it's NP-hard, with Provenance, we can reduce it to integer programming


# Sep. 8, 2021
1. find a naive alg to solve the problem
2. how to optimize it
3. time complexity
4. reduce another NPhard problem to our problem. try integer programming
5. see how Julia's paper does the reduction

# Sep. 13, 2021
1. understand the gap in overleaf doc, think of using bit arrays to solve it
2. write pseudo-code formally
3. complexity of naive solution
4. think of starting from conditions?

# Oct. 13, 2021
1. We now have the equations expressing our problems using provenance.
2. But if we want to use integer programming, we need to run it multiple times.
3. Did you really find resources to get multiple solutions of integer programming??????
4. Now forget about integer programming for now, but still use the expressions with provenance. Try to see whether there are other algorithms.
5. Skyline is the same as our original definition of minimality. But skyline problem is based on the assumption that we have a candidate dataset, and we want to find skyline from them. Now we don't have the candidate dataset. We use some constraints to find the candidate...
6. Try other algorithms???


# Oct. 20, 2021
Read reference papers again and see how they define, how they solved the problems...


# Oct. 22, 2021
Reading papers 

## Interactive Query Refinement,EDBT 2009
    - definequery refinements for categorical and numeric attributes.  
    Numeric: assume numeric predicates all have been transformed into $x_i < C_i$  
    Categorical: expansion/roll-up, shrinking/drill-down. 
    - main idea: find bounding query which has maximal relaxation for every attribtue.   
    Then for numeric attribute: let the user give a relaxation for one attribtue, the system compute a smaller bounding ranges based on binary search for other attributes, and let the user give a relaxation for another attribute.   
    For categorical attributes: user chooses one, and the system narrows down the selection based on the choice.

    - optimal: round robin with the user

    - Cardinality estimation scheme (SSE): estimate cardinality using sampling
    - SnS framework for query refinement: 
        1. Phase 1:  
            compute bounds. estimate the cardinality of the original query to see whether to relax or contract.  
            compute maximal relaxations along each dimension and generate bounding query $Q^b$.  
        2. Phase 2:  
            Use $Q^b$ as input, use SSE to compute $E_{Q^b}$ and use it to estimate cardinality of other queries.  
            This requires user interaction to capture user preference.

    - Phase 1: computing bounding query $Q^b$ (maximal relaxation)
        - numeric: binary search, cardinality estimator
        - categorical: compute number of tuples for each level
    - Phase 2: query refinement
        






## Relaxing  Join and Selection Queries, VLDB 2006

- main idea: relax queries involving joins and selections.  
Use a lattice to relax queries.

- optimality: assign weights to conditions

- Alg for relaxation skyline for relaxing selection conditions.

    - JoinFirst: compute the join, and compute the skyline in these tuples (standard skyline alg)
    - Pruning Join: discard dominated items
    - PruningJoin+: compute local relaxation skyline with dominance checking



- Alg for relaxing all conditions

    - MIDIR: traverse two R-trees top-down, get pairs, and check dominance
    - MIDIR can be modified if the user doesn't want to relax some conditions
    

## QReIX: Generating  Meaningful Queries that Provide Cardinality Assurance.  SIGMOD 10 demo

- main idea: generate alternate queries that meet the cardinality and coseness criteria
    - generate a refined query space
    - search based on proximity

## On Saying " Enough Already!" in SQL
- main idea: stop after giving enough results
- Add Stop After statement
- conservative / aggressive stop placement

## Automated Ranking of Database Query results CIDR 2003

- main idea: develop database IDF similarity to rank


# Nov. 3, 2021
A possible algorithm:
- pattern graph    
- patterns consist of: A_1, A_2.... and numeric C, where C can only equal some values depending on the dataset



# Nov. 5, 2021
Make some slides to include:     
- problem definition
- provenance expressions 
- the above algorithm   
We will talk with jag or julia


# Nov. 8, 2021
1. Stop implementing too many details
2. Read papers from Julia, and see what dataset/preprocessing they use. http://cidrdb.org/cidr2021/papers/cidr2021_paper27.pdf
3. Read paper from chapman
4. Meet with Julia Wed 1pm


# Nov. 10, 2021
1. Paper from Julia http://cidrdb.org/cidr2021/papers/cidr2021_paper27.pdf:
They have join and group by in preprocessing.
It has select by counties of interest.

# Feb 1, 2022
1. read those related papers
2. constraint satisfaction problem.
3. use the presentation we have now by provenance
4. look for a notebook with selection/deletion to use the dataset. See related work.
   see what operations are used in those notebooks and whether we can support


