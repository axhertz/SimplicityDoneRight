select count(*) from 
cast_info AS ci 
join role_type AS rt on (rt.role ='actress' AND rt.id = ci.role_id and ci.note = '(voice)')
join title AS t on (t.production_year BETWEEN 2007 AND 2008 AND t.title LIKE '%Kung%Fu%Panda%' AND t.id = ci.movie_id)
join name AS n on (n.gender ='f' AND n.name LIKE '%Angel%' AND n.id = ci.person_id)
join char_name AS chn on (chn.id = ci.person_role_id)
JOIN aka_name AS an  
on(an.person_id = ci.person_id)
join
 (select movie_id from movie_companies AS mc 
join company_name AS cn on (cn.country_code ='[us]' AND cn.id = mc.company_id and mc.note LIKE '%(200%)%' AND (mc.note LIKE '%(USA)%' OR mc.note LIKE '%(worldwide)%'))) as t_mc 
on(t_mc.movie_id = ci.movie_id)
join
 (select movie_id from movie_info AS mi 
join info_type AS it on (it.info = 'release dates' AND it.id = mi.info_type_id and mi.info IS NOT NULL AND (mi.info LIKE 'Japan:%2007%' OR mi.info LIKE 'USA:%2008%'))) as t_mi 
on(t_mi.movie_id = t_mc.movie_id)