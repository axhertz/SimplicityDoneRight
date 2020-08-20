select count(*) from 
cast_info AS ci 
join role_type AS rt on (rt.role ='actress' AND ci.role_id = rt.id and ci.note IN ('(voice)', '(voice: Japanese version)', '(voice) (uncredited)', '(voice: English version)'))
join name AS n on (n.gender ='f' AND n.name LIKE '%An%' AND n.id = ci.person_id)
join char_name AS chn on (chn.id = ci.person_role_id)
join title AS t on (ci.movie_id = t.id)
JOIN aka_name AS an  
on(an.person_id = ci.person_id)
JOIN movie_companies AS mc  
on(mc.movie_id = ci.movie_id)
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id);