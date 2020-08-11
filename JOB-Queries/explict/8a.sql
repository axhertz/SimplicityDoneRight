select count(*) from 
cast_info AS ci 
join role_type AS rt on (rt.role ='actress' AND ci.role_id = rt.id and ci.note ='(voice: English version)')
join name AS n1 on (n1.name LIKE '%Yo%' AND n1.name NOT LIKE '%Yu%' AND n1.id = ci.person_id)
join title AS t on (ci.movie_id = t.id)
JOIN aka_name AS an1  
on(an1.person_id = ci.person_id)
JOIN movie_companies AS mc  
on(mc.movie_id = ci.movie_id and mc.note LIKE '%(Japan)%' AND mc.note NOT LIKE '%(USA)%')
join company_name AS cn on (cn.country_code ='[jp]' AND mc.company_id = cn.id)