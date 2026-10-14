# Fabric notebook (PySpark), attached to the gold lakehouse
# Synthetic example. The newer gold layer already fixes most of what the old pbi.* tables get wrong.
from pyspark.sql import functions as F

silver_users = spark.table("silver.crm_users")
market_map = spark.table("gold.market_variant_map")

dim_customer = (
    silver_users
    .join(market_map, silver_users.market_name == market_map.variant_name, "left")
    .withColumn("customer_key", F.monotonically_increasing_id() + 1)
    .withColumn("signup_date", F.to_date("signup_ts"))
    .withColumn("postal_code", F.lpad(F.col("postal_code").cast("string"), 5, "0"))
    .select("customer_key", "email", "first_name", "last_name", "company_name", "job_title",
            "market_key", "city", "state", "postal_code", "signup_date", "is_enterprise")
)
dim_customer.write.mode("overwrite").format("delta").saveAsTable("gold.dim_customer")

unknown = spark.createDataFrame([(-1, "unknown@unknown.example")], "customer_key INT, email STRING")
unknown.write.mode("append").format("delta").saveAsTable("gold.dim_customer")
