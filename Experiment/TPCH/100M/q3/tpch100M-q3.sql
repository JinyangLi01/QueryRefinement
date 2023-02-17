-- TPC TPC-H Parameter Substitution (Version 3.0.0 build 0)
-- using 1674534801 as a seed to the RNG
-- $ID$
-- TPC-H/TPC-R Shipping Priority Query (Q3)
-- Functional Query Definition
-- Approved February 1998


select *
from
	customer,
	orders,
	lineitem
where
	c_mktsegment = 'BUILDING'
	and c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate < date '1995-03-28'
	and l_shipdate > date '1995-03-28'
;

