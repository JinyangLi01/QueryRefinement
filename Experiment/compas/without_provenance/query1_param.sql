select *
from
	compas
where
	`juv-fel-count` >= %(numeric1)s
    and `decile-score-x` >= %(numeric2)s
    and `r-charge-degree` in %(categorical1)s;

