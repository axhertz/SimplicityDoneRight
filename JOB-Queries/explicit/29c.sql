select count(*) from 
cast_info AS ci 
join role_type AS rt on (rt.role ='actress' AND rt.id = ci.role_id and ci.note IN ('(voice)', '(voice: Japanese version)', '(voice) (uncredited)', '(voice: English version)'))
join name AS n on (n.gender ='f' AND n.name LIKE '%An%' AND n.id = ci.person_id)
join title AS t on (t.production_year BETWEEN 2000 AND 2010 AND t.id = ci.movie_id)
join char_name AS chn on (chn.id = ci.person_role_id)
join
 (select movie_id from complete_cast AS cc 
join comp_cast_type AS cct2 on (cct2.kind ='complete+verified' AND cct2.id = cc.status_id)
join comp_cast_type AS cct1 on (cct1.kind ='cast' AND cct1.id = cc.subject_id)) as t_cc 
on(t_cc.movie_id = ci.movie_id)
JOIN aka_name AS an  
on(an.person_id = ci.person_id)
JOIN movie_companies AS mc  
on(mc.movie_id = t_cc.movie_id)
join company_name AS cn on (cn.country_code ='[us]' AND cn.id = mc.company_id)
join
 (select movie_id from movie_keyword AS mk 
join keyword AS k on (k.keyword = 'computer-animation' AND k.id = mk.keyword_id)) as t_mk 
on(t_mk.movie_id = mc.movie_id)
join
 (select person_id from person_info AS pi 
join info_type AS it3 on (it3.info = 'trivia' AND it3.id = pi.info_type_id)) as t_pi 
on(t_pi.person_id = ci.person_id)
join
 (select movie_id from movie_info AS mi 
join info_type AS it on (it.info = 'release dates' AND it.id = mi.info_type_id and mi.info IS NOT NULL AND (mi.info LIKE 'Japan:%200%' OR mi.info LIKE 'USA:%200%'))) as t_mi 
on(t_mi.movie_id = t_mk.movie_id);