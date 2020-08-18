select count(*) from 
movie_keyword AS mk 
join keyword AS k on (k.keyword IN ('sequel', 'revenge', 'based-on-novel') AND mk.keyword_id = k.id)
join title AS t on (t.production_year > 1950 AND t.id = mk.movie_id)
JOIN movie_companies AS mc  
on(mc.movie_id = mk.movie_id and mc.note IS NOT NULL)
join company_type AS ct on (ct.kind != 'production companies' AND ct.kind IS NOT NULL AND mc.company_type_id = ct.id)
join company_name AS cn on (cn.country_code !='[pl]' AND mc.company_id = cn.id)
JOIN movie_link AS ml  
on(ml.movie_id = mc.movie_id)
join link_type AS lt on (lt.id = ml.link_type_id);