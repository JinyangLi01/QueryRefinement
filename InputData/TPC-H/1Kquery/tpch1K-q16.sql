-- TPC TPC-H Parameter Substitution (Version 3.0.0 build 0)
-- using 1674101240 as a seed to the RNG
-- $ID$
-- TPC-H/TPC-R Parts/Supplier Relationship Query (Q16)
-- Functional Query Definition
-- Approved February 1998


select
	p_brand,
	p_type,
	p_size,
	count(distinct ps_suppkey) as supplier_cnt
from
	partsupp,
	part
where
	p_partkey = ps_partkey
	and p_brand <> 'Brand#11'
	and p_type not like 'MEDIUM ANODIZED%'
	and p_size in (36, 27, 20, 10, 30, 35, 48, 1)
	and ps_suppkey not in (
		select
			s_suppkey
		from
			supplier
		where
			s_comment like '%Customer%Complaints%'
	)
group by
	p_brand,
	p_type,
	p_size
order by
	supplier_cnt desc,
	p_brand,
	p_type,
	p_size;
limit -1;

