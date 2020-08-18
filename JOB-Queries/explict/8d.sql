select count(*) from 
cast_info AS ci 
join role_type AS rt on (rt.role ='costume designer' AND ci.role_id = rt.id)
join title AS t on (ci.movie_id = t.id)
join name AS n1 on (n1.id = ci.person_id)
JOIN aka_name AS an1  
on(an1.person_id = ci.person_id)
JOIN movie_companies AS mc  
on(mc.movie_id = ci.movie_id)
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id);