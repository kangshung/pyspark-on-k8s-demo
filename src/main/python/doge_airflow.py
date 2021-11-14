import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--date")

    return parser.parse_args()


def get_spark():
    return SparkSession.builder \
        .config("parentProject", "pyspark-demo-project") \
        .appName("block_application") \
        .getOrCreate()


def load_bq_table(spark, table_id, today):
    return spark.read.format("bigquery") \
        .option("filter", f"DATE(timestamp) = '{today}'") \
        .option("maxParallelism", 8) \
        .load(table_id)


def process_data(doge_blocks):
    blocks = doge_blocks. \
        select(col("hash"),
               col("bits"),
               col("transaction_count"),
               substring(col("timestamp"), 0, 10).alias("block_date")) \
        .coalesce(1)

    blocks.cache()

    return blocks


def save_df_to_gcs(df, today):
    df.write.format("avro") \
        .partitionBy('transaction_count') \
        .mode("overwrite") \
        .save(f"gs://pyspark-demo-data/block_application/date={today}")


def save_df_to_bq(df, today):
    df.write.format("bigquery") \
        .option("temporaryGcsBucket", "pyspark-demo-data") \
        .option("intermediateFormat", "avro") \
        .option("datePartition", f"{today}".replace("-", "")) \
        .mode("overwrite") \
        .save("pyspark-demo-project.doge.doge_blocks")


def main():
    spark = get_spark()
    args = get_args()
    today = args.date

    doge_blocks = load_bq_table(spark, "bigquery-public-data.crypto_dogecoin.blocks", today)

    blocks = process_data(doge_blocks)

    save_df_to_gcs(blocks, today)
    save_df_to_bq(blocks, today)

    spark.stop()


if __name__ == "__main__":
    main()
