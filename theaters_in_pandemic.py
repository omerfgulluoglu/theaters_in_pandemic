from pandasql import sqldf
import pandas as pd
import instaloader
from instaloader import Instaloader, Profile
import time
def query(q):
    return sqldf(q, globals())

import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

tiyatro = pd.read_csv('theater_play.csv')

q = """
select * from tiyatro
"""
query(q)

q = """
select * from (
select distinct THEATER_NAME, LONGITUDE, LATITUDE
from tiyatro
where 1=1
and substr(PLAY_DATE,1,4) not in ('2020','2019')
and substr(THEATER_NAME,1,4) not in ('BOZ,','ISTA','None')
limit 12) where substr(THEATER_NAME,1,21) not in ('Kağıthane Küçük Kemal','Gaziosmanpaşa Ferih E')
"""
sahneler = query(q)

sahneler

q = """
select substr(PLAY_DATE,1,4) as year,
substr(PLAY_DATE,6,2) as month, 
sum(NUMBER_OF_AUDIENCE) as talep
from tiyatro a
left join sahneler b on a.LONGITUDE=b.LONGITUDE and a.LATITUDE=b.LATITUDE
where 1=1
group by 1,2
order by 1,2
"""
query(q)

q = """
select substr(PLAY_DATE,1,4) as year,
substr(PLAY_DATE,6,2) as month, 
sum(NUMBER_OF_AUDIENCE) as talep
from tiyatro a
left join sahneler b on a.LONGITUDE=b.LONGITUDE and a.LATITUDE=b.LATITUDE
where 1=1
group by 1,2
order by 1,2
"""
query(q)
sns.catplot(x="month", y="talep",hue="year", data=query(q))

q = """
select substr(PLAY_DATE,1,4) as year,
substr(PLAY_DATE,6,2) as month,
PLAY_CATEGORY,
sum(NUMBER_OF_AUDIENCE) as talep
from tiyatro a
left join sahneler b on a.LONGITUDE=b.LONGITUDE and a.LATITUDE=b.LATITUDE
where 1=1
group by 1,2
order by 1,2
"""
query(q)

sns.set_style("whitegrid")
plt.figure(figsize=(15,10))
sns.barplot(x=query(q)['month'],
            y=query(q)['talep'],
            hue=query(q)['year'],
            data=query(q),
            ci=None
            #estimator=scalar
            #palettepalette=query(q)['yearmonth']
           )


q = """
select substr(PLAY_DATE,1,4) as year,
b.THEATER_NAME as tiyatro,
sum(NUMBER_OF_AUDIENCE) as talep
from tiyatro a
left join sahneler b on a.LONGITUDE=b.LONGITUDE and a.LATITUDE=b.LATITUDE
where 1=1
and substr(PLAY_DATE,1,4) <> '2017'
group by 1,2
order by 1,2
"""
query(q)

sns.set_style("whitegrid")
plt.figure(figsize=(15,10))
sns.barplot(x=query(q)['tiyatro'],
            y=query(q)['talep'],
            hue=query(q)['year'],
            data=query(q),
            ci=None
            #estimator=scalar
            #palettepalette=query(q)['yearmonth']
           )
plt.xticks(rotation= 75);


q = """
select * from (
select * from (
select substr(PLAY_DATE,1,4) || substr(PLAY_DATE,6,2) as yearmonth,
substr(PLAY_DATE,1,4) as year,
sum(NUMBER_OF_AUDIENCE) as talep
from tiyatro a
left join sahneler b on a.LONGITUDE=b.LONGITUDE and a.LATITUDE=b.LATITUDE
where 1=1
group by 1,2
order by 1,2)
union all select '202004' as yearmonth, '2020' as year, 0 as talep
union all select '202005' as yearmonth, '2020' as year, 0 as talep
union all select '202006' as yearmonth, '2020' as year, 0 as talep)
order by 1
"""
query(q)

sns.set_style("whitegrid")
plt.figure(figsize=(15,10))
sns.barplot(x=query(q)['yearmonth'],
            y=query(q)['talep'],
            hue=query(q)['year'],
            data=query(q),
            ci=None
            #estimator=scalar
            #palettepalette=query(q)['yearmonth']
           )
plt.xticks(rotation= 75);


q = """
select yearmonth, year, sum(talep*bilet_fiyati) as hasilat from (
select substr(PLAY_DATE,1,4) || substr(PLAY_DATE,6,2) as yearmonth,
substr(PLAY_DATE,1,4) as year,
PLAY_TYPE as tiyatro,
NUMBER_OF_AUDIENCE as talep,
case 
when PLAY_CATEGORY = 'Yetişkin' and substr(PLAY_DATE,1,4) in ('2020','2019') then 20
when PLAY_CATEGORY = 'Müzikal' and substr(PLAY_DATE,1,4) in ('2020','2019') then 27
when PLAY_CATEGORY = 'Çocuk' and substr(PLAY_DATE,1,4) in ('2020','2019') then 5
when PLAY_CATEGORY = 'Yetişkin' and substr(PLAY_DATE,1,4) = '2018' then 18
when PLAY_CATEGORY = 'Müzikal' and substr(PLAY_DATE,1,4) = '2018' then 24
when PLAY_CATEGORY = 'Çocuk' and substr(PLAY_DATE,1,4) = '2018' then 5
when PLAY_CATEGORY = 'Yetişkin' and substr(PLAY_DATE,1,4) = '2017' then 18
when PLAY_CATEGORY = 'Müzikal' and substr(PLAY_DATE,1,4) = '2017' then 22
when PLAY_CATEGORY = 'Çocuk' and substr(PLAY_DATE,1,4) = '2017' then 5 end as bilet_fiyati
from tiyatro)
group by 1
order by 1
"""
query(q)


sns.set_style("whitegrid")
plt.figure(figsize=(15,10))
sns.barplot(x=query(q)['yearmonth'],
            y=query(q)['hasilat'],
            hue=query(q)['year'],
            data=query(q),
            ci=None
            #estimator=scalar
            #palettepalette=query(q)['yearmonth']
           )
plt.xticks(rotation= 75);

q = """
select year, sum(talep*bilet_fiyati) as hasilat from (
select substr(PLAY_DATE,1,4) || substr(PLAY_DATE,6,2) as yearmonth,
substr(PLAY_DATE,1,4) as year,
PLAY_TYPE as tiyatro,
NUMBER_OF_AUDIENCE as talep,
case 
when PLAY_CATEGORY = 'Yetişkin' and substr(PLAY_DATE,1,4) in ('2020','2019') then 20
when PLAY_CATEGORY = 'Müzikal' and substr(PLAY_DATE,1,4) in ('2020','2019') then 27
when PLAY_CATEGORY = 'Çocuk' and substr(PLAY_DATE,1,4) in ('2020','2019') then 5
when PLAY_CATEGORY = 'Yetişkin' and substr(PLAY_DATE,1,4) = '2018' then 18
when PLAY_CATEGORY = 'Müzikal' and substr(PLAY_DATE,1,4) = '2018' then 24
when PLAY_CATEGORY = 'Çocuk' and substr(PLAY_DATE,1,4) = '2018' then 5
when PLAY_CATEGORY = 'Yetişkin' and substr(PLAY_DATE,1,4) = '2017' then 18
when PLAY_CATEGORY = 'Müzikal' and substr(PLAY_DATE,1,4) = '2017' then 22
when PLAY_CATEGORY = 'Çocuk' and substr(PLAY_DATE,1,4) = '2017' then 5 end as bilet_fiyati
from tiyatro)
where yearmonth = '201912'
group by 1
order by 1
"""
query(q)
