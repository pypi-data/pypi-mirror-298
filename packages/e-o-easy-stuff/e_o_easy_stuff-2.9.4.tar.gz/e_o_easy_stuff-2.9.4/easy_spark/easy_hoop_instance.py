from pyspark.sql import SparkSession
from py4j.java_gateway import java_import

from easy_spark.spark_instance import SparkInstance


class EasyHadoopInstance:
    _instance: 'EasyHadoopInstance' = None
    _hadoop_conf = None
    _fs = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            if args[0]:
                SparkInstance(args[0])
            must_java_import = args[1]

            if must_java_import:
                cls.import_java()

            cls.configure_fs()

            cls._instance = super(EasyHadoopInstance, cls).__new__(cls)
        return cls._instance

    def __init__(self, spark: SparkSession = None, must_java_import=True):
        self.hadoop_conf = EasyHadoopInstance._hadoop_conf
        self.fs = EasyHadoopInstance._fs
        pass

    @classmethod
    def import_java(cls):
        spark = SparkInstance.get_spark()
        java_import(spark._jvm, 'org.apache.hadoop.fs.FileSystem')
        java_import(spark._jvm, 'org.apache.hadoop.conf.Configuration')
        java_import(spark._jvm, 'org.apache.hadoop.fs.Path')

    @classmethod
    def configure_fs(cls):
        spark = SparkInstance.get_spark()
        cls._hadoop_conf = spark._jsc.hadoopConfiguration()
        cls._fs = spark._jvm.FileSystem.get(cls._hadoop_conf)
