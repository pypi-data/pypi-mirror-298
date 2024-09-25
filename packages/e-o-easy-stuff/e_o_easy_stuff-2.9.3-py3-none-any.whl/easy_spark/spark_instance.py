from pyspark.sql import SparkSession


class SparkInstance:
    _instance: 'SparkInstance' = None
    _spark: SparkSession = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._spark = args[0]
            cls._instance = super(SparkInstance, cls).__new__(cls)
        return cls._instance

    def __init__(self, spark: SparkSession = None):
        self.spark = SparkInstance._spark
        pass

    # class method property
    @classmethod
    def get_spark(cls) -> SparkSession:
        return cls._spark
