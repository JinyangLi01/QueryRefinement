-- TPC TPC-H Parameter Substitution (Version 3.0.0 build 0)
-- using 1674534801 as a seed to the RNG
-- $ID$
-- TPC-H/TPC-R Returned Item Reporting Query (Q10)
-- Functional Query Definition
-- Approved February 1998


select *
from
	customer,
	orders,
	lineitem,
	nation
where
	c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate >= date '1993-02-01'
	and l_quantity < 20
	and l_returnflag = 'R'
	and c_nationkey = n_nationkey
;

