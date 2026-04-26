# Databricks notebook source
from pyspark.sql.types import *
from pyspark.sql.functions import *

# COMMAND ----------

df = spark.read.table("uber.bronze.bulk_rides")

# COMMAND ----------

rides_schema = StructType([StructField('ride_id', StringType(), True), StructField('confirmation_number', StringType(), True), StructField('passenger_id', StringType(), True), StructField('driver_id', StringType(), True), StructField('vehicle_id', StringType(), True), StructField('pickup_location_id', StringType(), True), StructField('dropoff_location_id', StringType(), True), StructField('vehicle_type_id', LongType(), True), StructField('vehicle_make_id', LongType(), True), StructField('payment_method_id', LongType(), True), StructField('ride_status_id', LongType(), True), StructField('pickup_city_id', LongType(), True), StructField('dropoff_city_id', LongType(), True), StructField('cancellation_reason_id', LongType(), True), StructField('passenger_name', StringType(), True), StructField('passenger_email', StringType(), True), StructField('passenger_phone', StringType(), True), StructField('driver_name', StringType(), True), StructField('driver_rating', DoubleType(), True), StructField('driver_phone', StringType(), True), StructField('driver_license', StringType(), True), StructField('vehicle_model', StringType(), True), StructField('vehicle_color', StringType(), True), StructField('license_plate', StringType(), True), StructField('pickup_address', StringType(), True), StructField('pickup_latitude', DoubleType(), True), StructField('pickup_longitude', DoubleType(), True), StructField('dropoff_address', StringType(), True), StructField('dropoff_latitude', DoubleType(), True), StructField('dropoff_longitude', DoubleType(), True), StructField('distance_miles', DoubleType(), True), StructField('duration_minutes', LongType(), True), StructField('booking_timestamp', TimestampType(), True), StructField('pickup_timestamp', StringType(), True), StructField('dropoff_timestamp', StringType(), True), StructField('base_fare', DoubleType(), True), StructField('distance_fare', DoubleType(), True), StructField('time_fare', DoubleType(), True), StructField('surge_multiplier', DoubleType(), True), StructField('subtotal', DoubleType(), True), StructField('tip_amount', DoubleType(), True), StructField('total_fare', DoubleType(), True), StructField('rating', DoubleType(), True)])


# COMMAND ----------

df = spark.read.table("uber.bronze.rides_raw").select("rides")
df_parsed = df.withColumn("parsed_rides", from_json("rides", rides_schema))\
                .select(col("parsed_rides.*"))

# COMMAND ----------

display(df_parsed)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Jinja templating

# COMMAND ----------

# DBTITLE 1,Cell 7
jinja_config = [
    {
        "table" : "uber.bronze.stg_rides as stg_rides",
        "select" : "stg_rides.*",
        "where" :""
    },
    {
        "table": "uber.bronze.map_vehicle_types map_vehicle_types",
        "select" : "map_vehicle_types.vehicle_type",
        "where": "",
        "on": "stg_rides.vehicle_type_id = map_vehicle_types.vehicle_type_id"
    },
    {
        "table": "uber.bronze.map_vehicle_makes map_vehicle_makes",
        "select": "map_vehicle_makes.vehicle_make",
        "where":"",
        "on": "stg_rides.vehicle_make_id = map_vehicle_makes.vehicle_make_id"
    },
    {
        "table": "uber.bronze.map_payment_methods map_payment_methods",
        "select": "map_payment_methods.payment_method",
        "where":"",
        "on": "stg_rides.payment_method_id = map_payment_methods.payment_method_id"
    },
    {
        "table": "uber.bronze.map_ride_statuses map_ride_statuses",
        "select": "map_ride_statuses.ride_status",
        "where":"",
        "on": "stg_rides.ride_status_id = map_ride_statuses.ride_status_id"
    },
    {
        "table": "uber.bronze.map_cancellation_reasons map_cancellation_reasons",
        "select": "map_cancellation_reasons.cancellation_reason",
        "where":"",
        "on": "stg_rides.cancellation_reason_id = map_cancellation_reasons.cancellation_reason_id"
    }
]

# COMMAND ----------

from jinja2 import Template

jinga_str = '''
    SELECT 
        {% for config in jinga_config %}
            {{config.select}} 
                {% if not loop.last %} , {% endif %}
        {% endfor %}
    FROM 
        {% for config in jinga_config %}
            {% if loop.first %}
                {{config.table}}
            {% else  %}
                LEFT JOIN {{config.table}} ON {{config.on}}
            {% endif %}
        {% endfor %}
    {% for config in jinga_config %}
        {% if loop.first %}
            {% if config.where != '' %}
                WHERE   
            {% endif %}
        {% else  %}
            {{config.where}}
            {% if not loop.last %} 
                {% if config.where != '' %}
                    AND 
                {% endif %}
            {% endif %}
        {% endif %}
    {% endfor %}
'''

# COMMAND ----------

template = Template(jinga_str)
query = template.render(jinga_config=jinja_config)
print(query)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   stg_rides.*
# MAGIC FROM
# MAGIC   uber.bronze.stg_rides stg_rides
# MAGIC LEFT JOIN
# MAGIC   uber.bronze.map_vehicle_types map_vehicle_types
# MAGIC ON
# MAGIC   stg_rides.vehicle_type_id = map_vehicle_types.vehicle_type_id
# MAGIC LEFT JOIN
# MAGIC   uber.bronze.map_vehicle_makes map_vehicle_makes
# MAGIC ON
# MAGIC   stg_rides.vehicle_make_id = map_vehicle_makes.vehicle_make_id
# MAGIC   

# COMMAND ----------

df_q = spark.sql(query)
display(df_q)

# COMMAND ----------

df_q.columns

# COMMAND ----------

# %sql
# drop table uber.bronze.stg_rides

# COMMAND ----------

