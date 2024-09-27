from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import col, regexp_replace
from datetime import datetime, date
import pandas as pd

def test_spark_dataframe():
    spark = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()
    df = spark.createDataFrame([
        Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
        Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
        Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
    ])
    print(df)
    spark.stop()

def test_spark_read_text():
    spark = SparkSession.builder.appName("ehtn_test").getOrCreate()

    text_data = spark.read.text('hdfs://10.224.81.60:8020/data0/plants/yangju/2021/2021_01/2021_01_27/GTC1_11RCAOGC005_01.txt.gz')
    text_data.show()

    spark.stop()

def test_spark_dataframe2():
    spark = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()

    sample_data = [{"name": "John    D.", "age": 30},
                   {"name": "Alice   G.", "age": 25},
                   {"name": "Bob  T.", "age": 35},
                   {"name": "Eve   A.", "age": 28}]

    df = spark.createDataFrame(sample_data)

    def remove_extra_spaces(df, column_name):
        df_transformed = df.withColumn(column_name, regexp_replace(col(column_name), "\\s+", " "))
        return df_transformed

    transformed_df = remove_extra_spaces(df, "name")
    transformed_df.show()
    spark.stop()
