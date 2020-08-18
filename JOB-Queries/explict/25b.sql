select count(*) from 
movie_info_idx AS mi_idx 
join info_type AS it2 on (it2.info = 'votes' AND it2.id = mi_idx.info_type_id)
join title AS t on (t.production_year > 2010 AND t.title LIKE 'Vampire%' AND t.id = mi_idx.movie_id)
join
 (select movie_id from movie_keyword AS mk 
join keyword AS k on (k.keyword IN ('murder', 'blood', 'gore', 'death', 'female-nudity') AND k.id = mk.keyword_id)) as t_mk 
on(t_mk.movie_id = mi_idx.movie_id)
join
 (select person_id, movie_id from cast_info AS ci 
join name AS n on (n.gender = 'm' AND n.id = ci.person_id and ci.note IN ('(writer)', '(head writer)', '(written by)', '(story)', '(story editor)'))) as t_ci 
on(t_ci.movie_id = t_mk.movie_id)
JOIN movie_info AS mi  
on(mi.movie_id = t_ci.movie_id and mi.info = 'Horror')
join info_type AS it1 on (it1.info = 'genres' AND it1.id = mi.info_type_id);