select count(*) from 
complete_cast AS cc 
join comp_cast_type AS cct1 on (cct1.kind = 'cast' AND cct1.id = cc.subject_id)
join comp_cast_type AS cct2 on (cct2.kind LIKE '%complete%' AND cct2.id = cc.status_id)
join title AS t on (t.production_year > 2000 AND t.id = cc.movie_id)
join kind_type AS kt on (kt.kind = 'movie' AND kt.id = t.kind_id)
join
 (select movie_id from movie_keyword AS mk 
join keyword AS k on (k.keyword IN ('superhero', 'sequel', 'second-part', 'marvel-comics', 'based-on-comic', 'tv-special', 'fight', 'violence') AND k.id = mk.keyword_id)) as t_mk 
on(t_mk.movie_id = cc.movie_id)
join
 (select person_id, movie_id from cast_info AS ci 
join name AS n on (n.name LIKE '%Downey%Robert%' AND n.id = ci.person_id)
join char_name AS chn on (chn.name NOT LIKE '%Sherlock%' AND (chn.name LIKE '%Tony%Stark%' OR chn.name LIKE '%Iron%Man%') AND chn.id = ci.person_role_id)) as t_ci 
on(t_ci.movie_id = t_mk.movie_id)