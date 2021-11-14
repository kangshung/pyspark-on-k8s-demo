from datetime import date

from pyspark.sql import SparkSession


def get_spark():
    return SparkSession.builder \
        .config("parentProject", "pyspark-demo-project") \
        .appName("doge_app") \
        .getOrCreate()


def load_bq_table(spark, table_id, month="2021-01-01"):
    return spark.read.format("bigquery") \
        .option("filter", f"timestamp_month = '{month}'") \
        .option("maxParallelism", 4) \
        .load(table_id)


def process_data(doge_blocks):
    doge_grouped = doge_blocks.groupBy("version").count().coalesce(1)

    doge_grouped.cache()

    return doge_grouped


def save_df_to_gcs(df):
    df.write.format("avro") \
        .mode("overwrite") \
        .save(f"gs://pyspark-demo-data/date={date.today()}")


def save_df_to_bq(df):
    df.write.format("bigquery") \
        .option("temporaryGcsBucket", "pyspark-demo-data") \
        .option("intermediateFormat", "avro") \
        .mode("append") \
        .save("pyspark-demo-project.doge.doge_grouped")


def main():
    spark = get_spark()
    doge_blocks = load_bq_table(spark, "bigquery-public-data.crypto_dogecoin.blocks")

    doge_grouped = process_data(doge_blocks)

    save_df_to_gcs(doge_grouped)
    save_df_to_bq(doge_grouped)

    spark.stop()


if __name__ == "__main__":
    main()
