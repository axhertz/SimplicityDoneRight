select count(*) from 
movie_info AS mi 
join title AS t on (t.production_year > 2005 AND t.id = mi.movie_id and mi.info IN ('Sweden','Norway', 'Germany', 'Denmark', 'Swedish','Denish', 'Norwegian', 'German'))
JOIN movie_keyword AS mk  
on(mk.movie_id = mi.movie_id)
join keyword AS k on (k.keyword LIKE '%sequel%' AND k.id = mk.keyword_id);