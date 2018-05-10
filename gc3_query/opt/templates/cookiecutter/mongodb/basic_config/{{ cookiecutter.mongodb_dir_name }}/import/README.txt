Database exports can be imported using something like the following (Mongodb must be running):

mongorestore /host:127.0.0.1 /port:7117 --drop --db bookstore C:\Users\emharris\devel\gc3-query\gc3_query\var\mongodb\import\bookstore
