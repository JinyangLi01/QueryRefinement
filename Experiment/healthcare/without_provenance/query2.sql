select *
from
	healthcare
where
	income >= 150 and num_children <= 4 and complications <= 8
    and county in ('county2', 'county4');

