from pyspark.sql import SparkSession

def test_func():
    print("test_func")

def test_func2():
    print("test_func2 start")

    spark = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()
    spark.stop()

    print("test_func2 end")