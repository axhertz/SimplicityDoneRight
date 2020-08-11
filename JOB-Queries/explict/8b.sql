select count(*) from 
cast_info AS ci 
join role_type AS rt on (rt.role ='actress' AND ci.role_id = rt.id and ci.note ='(voice: English version)')
join name AS n on (n.name LIKE '%Yo%' AND n.name NOT LIKE '%Yu%' AND n.id = ci.person_id)
join title AS t on (t.production_year BETWEEN 2006 AND 2007 AND (t.title LIKE 'One Piece%' OR t.title LIKE 'Dragon Ball Z%') AND ci.movie_id = t.id)
JOIN aka_name AS an  
on(an.person_id = ci.person_id)
JOIN movie_companies AS mc  
on(mc.movie_id = ci.movie_id and mc.note LIKE '%(Japan)%' AND mc.note NOT LIKE '%(USA)%' AND (mc.note LIKE '%(2006)%' OR mc.note LIKE '%(2007)%'))
join company_name AS cn on (cn.country_code ='[jp]' AND mc.company_id = cn.id)