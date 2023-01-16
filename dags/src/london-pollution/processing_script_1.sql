BEGIN;

select date(slp.timestamp), extract(hour from slp.timestamp) as "hour", city.id as city_id, country.id as country_id, temp_c, humidity, co, no2, o3, so2, pm2_5, pm10
into temp.london_pollution
from staging.london_pollution slp
inner join public.countries country
on country.name = slp.country
inner join public.cities city
on city.name = slp.location;

INSERT INTO pollution.uk (date, "hour", city_id, country_id, temp_c, humidity, co, no2, o3, so2, pm2_5, pm10)
select date, "hour", city_id, country_id, temp_c, humidity, co, no2, o3, so2, pm2_5, pm10
from temp.london_pollution
ON CONFLICT (date, "hour", city_id, country_id) 
DO UPDATE 
SET 
temp_c = excluded.temp_c,
humidity = excluded.humidity,
co = excluded.co,
no2 = excluded.no2,
o3 = excluded.o3,
so2 = excluded.no2,
pm2_5 = excluded.pm2_5,
pm10 = excluded.pm10;

drop table temp.london_pollution;
truncate table staging.london_pollution;

COMMIT;