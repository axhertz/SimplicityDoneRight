select count(*) from 
movie_companies AS mc 
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id)
join title AS t on (t.id = mc.movie_id)
join
 (select person_id, movie_id from cast_info AS ci 
join role_type AS rt on (rt.role ='writer' AND ci.role_id = rt.id)
join name AS n1 on (n1.id = ci.person_id)) as t_ci 
on(t_ci.movie_id = mc.movie_id)
JOIN aka_name AS a1  
on(a1.person_id = t_ci.person_id);