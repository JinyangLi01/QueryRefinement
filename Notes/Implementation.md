# Mar 28, 2022
1. Optimization1: add label marking a row in sorted table is positive or negative.
  If we have both directions, we need to build a refinement based on both positive and negative terms.
  Otherwise it should be eliminated earlier.
2. Optimization2: for positive rows, zero column should be changed to -4 meaning if we want to refine this column, 
   it can't be more than 4.
3. Optimization3: Many categorical columns in sorted table have last part of repeating subsequence of the leftmost columns.
    Eg. leftmost row in sorted table is 164325, another column may be 164235
   or even the same. To avoid repeating checking the same subsequence, 
   1. delete a column if it is the same as the leftmost one
   2. compare with the leftmost column.
4. Optimization4: merge same terms in the same inequality.
5. Precision: int is 1, float is 0.05

# Apr 19, 2022

1. algorithm without optimization: ProvenanceSearch_3
2. algorithm without optimization 1: ProvenanceSearch_4
3. algorithm without optimization 1, 2: ProvenanceSearch_5
4. !!! example 2, selection 2, our alg missed a result?