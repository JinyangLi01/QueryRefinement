-- TPC TPC-H Parameter Substitution (Version 3.0.0 build 0)
-- using 1674534801 as a seed to the RNG
-- $ID$
-- TPC-H/TPC-R Minimum Cost Supplier Query (Q2)
-- Functional Query Definition
-- Approved February 1998


select *
from
	part,
	supplier,
	partsupp,
	nation,
	region
where
	p_partkey = ps_partkey
	and s_suppkey = ps_suppkey
	and p_size >= 42
	and p_type_suffix = 'STEEL'
	and s_nationkey = n_nationkey
	and n_regionkey = r_regionkey
	and r_name = 'MIDDLE EAST'
-- 	and ps_supplycost = (
-- 		select
-- 			min(ps_supplycost)
-- 		from
-- 			partsupp,
-- 			supplier,
-- 			nation,
-- 			region
-- 		where
-- 			p_partkey = ps_partkey
-- 			and s_suppkey = ps_suppkey
-- 			and s_nationkey = n_nationkey
-- 			and n_regionkey = r_regionkey
-- 			and r_name = 'MIDDLE EAST'
-- 	)
;

