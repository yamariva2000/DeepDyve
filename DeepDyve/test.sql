
alter table docs
add body text,
add publisher text,
add REFAUTHOR text,
add volissue text,
add title text,
add journal text,
add issn text,
add a_affiliation text,
add REFTITLE text,
add REFVOL text,
add authors text,
add sa text,
add id text;


update docs set
publisher = data->'publisher',
REFAUTHOR =data->'REFAUTHOR',
volissue=data->'volissue',
title=data->'title',
journal=data->'journal',
issn=data->'issn',
a_affiliation  = data ->'a_affiliation',
REFTITLE=data->'REFTITLE',
REFVOL=data->'REFVOL',
authors=data->'authors',
sa=data->'sa',
id=data->'id',
body=data->'body';


