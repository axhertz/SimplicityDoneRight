select count(*) from 
aka_name AS a1 
join
 (select person_id, movie_id from cast_info AS ci 
join role_type AS rt on (rt.role ='writer' AND ci.role_id = rt.id)
join title AS t on (ci.movie_id = t.id)
join name AS n1 on (n1.id = ci.person_id)) as t_ci 
on(t_ci.person_id = a1.person_id)
JOIN movie_companies AS mc  
on(mc.movie_id = t_ci.movie_id)
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id);