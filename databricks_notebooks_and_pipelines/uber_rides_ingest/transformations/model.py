from pyspark import pipelines as dp

@dp.view
def dim_passenger_view():
    df = spark.readStream.table("silver_obt")
    df = df.select("passenger_id", "passenger_name", "passenger_email","passenger_phone")
    df = df.dropDuplicates(subset = ["passenger_id"])
    return df


# DIM Passenger
dp.create_streaming_table("dim_passenger")

dp.create_auto_cdc_flow(
    target = "dim_passenger",
    source = "dim_passenger_view",
    keys = ["passenger_id"],
    sequence_by="passenger_id",
    stored_as_scd_type="1"
)



#DIM DRIVER
@dp.view
def dim_driver_view():
    df = spark.readStream.table("silver_obt")
    df = df.select("driver_id", "driver_name", "driver_rating","driver_phone","driver_license")
    df = df.dropDuplicates(subset = ["driver_id"])
    return df


# DIM Driver
dp.create_streaming_table("dim_driver")

dp.create_auto_cdc_flow(
    target = "dim_driver",
    source = "dim_driver_view",
    keys = ["driver_id"],
    sequence_by="driver_id",
    stored_as_scd_type="1"
)



#DIM VEHICLE
@dp.view
def dim_vehicle_view():
    df = spark.readStream.table("silver_obt")
    df = df.select("vehicle_id", "vehicle_make_id", "vehicle_make" ,"vehicle_type_id" ,"vehicle_model"
                   ,"vehicle_type")
    df = df.dropDuplicates(subset = ["vehicle_id"])
    return df

dp.create_streaming_table("dim_vehicle")

dp.create_auto_cdc_flow(
    target = "dim_vehicle",
    source = "dim_vehicle_view",
    keys = ["vehicle_id"],
    sequence_by="vehicle_id",
    stored_as_scd_type="1"
)


#DIM PAYMENTS
@dp.view
def dim_payment_view():
    df = spark.readStream.table("silver_obt")
    df = df.select("payment_method_id", "payment_method", "is_card" ,"requires_auth")
    df = df.dropDuplicates(subset = ["payment_id"])
    return df

dp.create_streaming_table("dim_payment")

dp.create_auto_cdc_flow(
    target = "dim_payment",
    source = "dim_payment_view",
    keys = ["payment_id"],
    sequence_by="payment_id",
    stored_as_scd_type="1"
)



#DIM LOCATION
@dp.table
def dim_location_table():
    df = spark.readStream.table("silver_obt")
    df = df.select("pickup_city_id", "pickup_city", "city_updated_at", "region", "state")
    df = df.dropDuplicates(subset = ["pickup_city_id", "city_updated_at"])
    return df

dp.create_streaming_table("dim_location")

dp.create_auto_cdc_flow(
    target = "dim_location",
    source = "dim_location_view",
    keys = ["city_id"],
    sequence_by="city_updated_at",
    stored_as_scd_type="2"
)





















