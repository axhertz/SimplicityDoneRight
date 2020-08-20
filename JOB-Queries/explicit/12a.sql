select count(*) from 
movie_info_idx AS mi_idx 
join info_type AS it2 on (it2.info = 'rating' AND mi_idx.info_type_id = it2.id and mi_idx.info > '8.0')
join title AS t on (t.production_year BETWEEN 2005 AND 2008 AND t.id = mi_idx.movie_id)
JOIN movie_info AS mi  
on(mi.movie_id = mi_idx.movie_id and mi.info IN ('Drama', 'Horror'))
join info_type AS it1 on (it1.info = 'genres' AND mi.info_type_id = it1.id)
JOIN movie_companies AS mc  
on(mc.movie_id = mi.movie_id)
join company_type AS ct on (ct.kind = 'production companies' AND ct.id = mc.company_type_id)
join company_name AS cn on (cn.country_code = '[us]' AND cn.id = mc.company_id);