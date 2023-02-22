-- TPC TPC-H Parameter Substitution (Version 3.0.0 build 0)
-- using 1676524598 as a seed to the RNG
-- $ID$
-- TPC-H/TPC-R Shipping Modes and Order Priority Query (Q12)
-- Functional Query Definition
-- Approved February 1998


select *
from
	orders,
	lineitem
where
	o_orderkey = l_orderkey
	and l_shipmode in ('FOB', 'MAIL')
	and l_commitdate < l_receiptdate
	and l_shipdate < l_commitdate
	and l_receiptdate >= date '1994-01-01'
	and l_shipdate < date '1995-01-01'
;
