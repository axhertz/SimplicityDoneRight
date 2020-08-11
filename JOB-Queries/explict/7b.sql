select count(*) from 
movie_link AS ml 
join link_type AS lt on (lt.link ='features' AND lt.id = ml.link_type_id)
join title AS t on (t.production_year BETWEEN 1980 AND 1984 AND ml.linked_movie_id = t.id)
JOIN cast_info AS ci  
on(ci.movie_id = ml.linked_movie_id)
join name AS n on (n.name_pcode_cf LIKE 'D%' AND n.gender='m' AND ci.person_id = n.id)
JOIN person_info AS pi  
on(pi.person_id = ci.person_id and pi.note ='Volker Boehm')
join info_type AS it on (it.info ='mini biography' AND it.id = pi.info_type_id)
JOIN aka_name AS an  
on(an.person_id = pi.person_id and an.name LIKE '%a%')
