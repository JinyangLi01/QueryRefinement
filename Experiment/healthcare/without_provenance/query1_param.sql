select *
from
	healthcare
where
	income >= %(numeric1)s
    and `num-children` >= %(numeric2)s
    and county in %(categorical1)s;

