import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://my-datapipeline-bucket/data/customers.csv"]},
    format="csv",
    format_options={"withHeader": True}
)

filtered = Filter.apply(frame=datasource, f=lambda x: x["country"] == "USA")

sink = glueContext.getSink(
    path="s3://my-datapipeline-bucket/processed/customers_usa/",
    connection_type="s3",
    updateBehavior="LOG",
    partitionKeys=["state"],
    enableUpdateCatalog=True
)
sink.setFormat("parquet")
sink.writeFrame(filtered)
