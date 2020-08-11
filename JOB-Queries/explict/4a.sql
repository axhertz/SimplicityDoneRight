select count(*) from 
movie_keyword AS mk 
join keyword AS k on (k.keyword LIKE '%sequel%' AND k.id = mk.keyword_id)
join title AS t on (t.production_year > 2005 AND t.id = mk.movie_id)
join
 (select movie_id from movie_info_idx AS mi_idx 
join info_type AS it on (it.info ='rating' AND it.id = mi_idx.info_type_id and mi_idx.info > '5.0')) as t_mi_idx 
on(t_mi_idx.movie_id = mk.movie_id)