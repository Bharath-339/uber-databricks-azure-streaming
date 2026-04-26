# Databricks notebook source
token =""

import pandas as pd

files = [
    {"fileName": "bulk_rides"},
    {"fileName": "map_cancellation_reasons"},
    {"fileName": "map_cities"},
    {"fileName": "map_payment_methods"},
    {"fileName": "map_ride_statuses"},
    {"fileName": "map_vehicle_makes"},
    {"fileName": "map_vehicle_types"}
]

url = "https://uberdatabricksstreaming.blob.core.windows.net/raw/ingestion"

# COMMAND ----------

file = "map_cities.json"
url_token = f"{url}/{file}?{token}"

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

# DBTITLE 1,Cell 4
import io
import requests

for file in files:
    fileName = file["fileName"]
    url_token = f"{url}/{fileName}.json?{token}"
    response = requests.get(url_token)
    content = response.text
    try:
        df = pd.read_json(io.StringIO(content), lines= True)
    except Exception as e:
        print(f"Error reading file {fileName}: {e}")
        continue
    df = spark.createDataFrame(df)
    df = df.withColumn("updated_at", current_timestamp())
    df.write.format("delta")\
            .mode("overwrite")\
            .option("overwriteschema",True)\
            .saveAsTable(f"uber.bronze.{fileName}")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from uber.bronze.map_cities

# COMMAND ----------

