select count(*) from 
movie_keyword AS mk 
join keyword AS k on (k.keyword IN ('murder',  'violence', 'blood', 'gore', 'death', 'female-nudity', 'hospital') AND k.id = mk.keyword_id)
join title AS t on (t.id = mk.movie_id)
join
 (select movie_id from movie_info_idx AS mi_idx 
join info_type AS it2 on (it2.info = 'votes' AND it2.id = mi_idx.info_type_id)) as t_mi_idx 
on(t_mi_idx.movie_id = mk.movie_id)
JOIN cast_info AS ci  
on(ci.movie_id = t_mi_idx.movie_id and ci.note IN ('(writer)', '(head writer)', '(written by)',  '(story)',  '(story editor)'))
join name AS n on (n.gender = 'm' AND n.id = ci.person_id)
JOIN movie_info AS mi  
on(mi.movie_id = ci.movie_id and mi.info IN ('Horror', 'Action', 'Sci-Fi', 'Thriller', 'Crime', 'War'))
join info_type AS it1 on (it1.info = 'genres' AND it1.id = mi.info_type_id)