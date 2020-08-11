select count(*) from 
movie_keyword AS mk 
join keyword AS k on (k.keyword LIKE '%sequel%' AND k.id = mk.keyword_id)
join title AS t on (t.production_year > 2005 AND t.id = mk.movie_id)
JOIN movie_info AS mi  
on(mi.movie_id = mk.movie_id and mi.info IN ('Sweden','Norway', 'Germany', 'Denmark', 'Swedish','Denish', 'Norwegian', 'German'))