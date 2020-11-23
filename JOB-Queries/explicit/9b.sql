select count(*) from 
movie_companies AS mc 
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id and mc.note LIKE '%(200%)%' AND (mc.note LIKE '%(USA)%' OR mc.note LIKE '%(worldwide)%'))
join title AS t on (t.production_year BETWEEN 2007 AND 2010 AND t.id = mc.movie_id)
JOIN cast_info AS ci  
on(ci.movie_id = mc.movie_id and ci.note = '(voice)')
join role_type AS rt on (rt.role ='actress' AND ci.role_id = rt.id)
join name AS n on (n.gender ='f' AND n.name LIKE '%Angel%' AND n.id = ci.person_id)
join char_name AS chn on (chn.id = ci.person_role_id)
JOIN aka_name AS an  
on(an.person_id = ci.person_id);