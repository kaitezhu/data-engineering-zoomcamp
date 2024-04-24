Question 3

select count(1)
from taxi_trips
where cast(lpep_pickup_datetime as date) = '2019-09-18'
and cast(lpep_dropoff_datetime as date) = '2019-09-18';

Question 4

select lpep_pickup_datetime, ((lpep_dropoff_datetime::timestamp) - (lpep_pickup_datetime::timestamp)) as timediff
from taxi_trips
order by timediff desc
limit 1;

