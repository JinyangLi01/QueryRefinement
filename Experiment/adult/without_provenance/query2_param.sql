select *
from
	adult
where
	`education-num` >= %(numeric1)s
    and `hours-per-week` <= %(numeric2)s
    and relationship in %(categorical1)s;

