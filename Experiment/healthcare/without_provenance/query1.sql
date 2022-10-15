select *
from
	healthcare
where
	income >= 100
    and `num-children` >= 3
    and county in ('county2', 'county3');

