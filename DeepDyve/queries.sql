

select count(journal) as unique_journals from (

select journal from docs group by journal) as foo;




select publisher from docs group by publisher;

--    publisher
-----------------------------
-- "North-Holland"
-- "Cell Press"
-- "Pergamon"
-- "Churchill Livingstone"
-- "W.B. Saunders"
-- ""
-- "Excerpta Medica"
-- "Elsevier"
-- "Elsevier Current Trends"
-- "Mosby"
-- "Academic Press"


select publisher,count(*) from docs group by publisher;


--publisher         | count
-----------------------------+--------
-- "North-Holland"           |   2531
-- "Cell Press"              |    907
-- "Pergamon"                |   1163
-- "Churchill Livingstone"   |     79
-- "W.B. Saunders"           |     48
-- ""                        |     54
-- "Excerpta Medica"         |     87
-- "Elsevier"                | 192489
-- "Elsevier Current Trends" |    319
-- "Mosby"                   |    557
-- "Academic Press"          |   1766

select count(* as )
select sa, count(*) from docs group by sa;




