import psycopg2

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
conn=psycopg2.connect(user='kelster', password='CookieDoge',
                                host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve')
c=conn.cursor()


#sql='select subjects_arr, count(*) as documents from docs group by subjects_arr order by documents'

sql="select subject1 as subject ,count(*) from docs group by subject1 order by count(*) desc;"
result=c.execute(sql)

#print c.fetchmany(100)


df=pd.read_sql(sql,conn)

print df

sb.boxplot(x=df['subject'],y=df['count'])

plt.plot(x=df['subject'],y=df['count'])

plt.show()

