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
5. Precision: int is 1, float is 0.05.

# Apr 19, 2022

1. algorithm without optimization: ProvenanceSearch_3
2. algorithm with optimization 1: ProvenanceSearch_4
3. algorithm with optimization 1, 2: ProvenanceSearch_5



# Apr 21, 2022
1. algorithm with optimization 1, 2, 4: ProvenanceSearch_8


# Apr 25, 2022 Jag's comments
1. predict when it takes long time, and use naive method instead
2. say that we win often, sometimes lose
3. avoid some traversal which I'm already doing



# May 3, 2022
1. relax-only is ok now. Theoretically there are cases with a large number of terms combinations to check, 
but I haven't encountered this with three small dataset for now.
2. I'm doing bidirectional.











# Experiments

## healthcare
1. round income to the nearest thousand

## TPCH
too slow both programs...



# general refinement
1. Things that don't work: 