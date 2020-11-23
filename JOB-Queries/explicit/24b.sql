select count(*) from 
movie_companies AS mc 
join company_name AS cn on (cn.country_code ='[us]' AND cn.name = 'DreamWorks Animation' AND cn.id = mc.company_id)
join title AS t on (t.production_year > 2010 AND t.title LIKE 'Kung Fu Panda%' AND t.id = mc.movie_id)
join
 (select movie_id from movie_keyword AS mk 
join keyword AS k on (k.keyword IN ('hero', 'martial-arts', 'hand-to-hand-combat', 'computer-animated-movie') AND k.id = mk.keyword_id)) as t_mk 
on(t_mk.movie_id = mc.movie_id)
join
 (select person_id, movie_id from cast_info AS ci 
join role_type AS rt on (rt.role ='actress' AND rt.id = ci.role_id and ci.note IN ('(voice)', '(voice: Japanese version)', '(voice) (uncredited)',  '(voice: English version)'))
join name AS n on (n.gender ='f' AND n.name LIKE '%An%' AND n.id = ci.person_id)
join char_name AS chn on (chn.id = ci.person_role_id)) as t_ci 
on(t_ci.movie_id = t_mk.movie_id)
JOIN aka_name AS an  
on(an.person_id = t_ci.person_id)
join
 (select movie_id from movie_info AS mi 
join info_type AS it on (it.info = 'release dates' AND it.id = mi.info_type_id and mi.info IS NOT NULL AND (mi.info LIKE 'Japan:%201%' OR mi.info LIKE 'USA:%201%'))) as t_mi 
on(t_mi.movie_id = t_ci.movie_id);