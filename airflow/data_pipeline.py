from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator
from airflow.utils.dates import days_ago

with DAG(
    'data_pipeline',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False
) as dag:

    glue_etl = AwsGlueJobOperator(
        task_id='run_glue_etl',
        job_name='my-glue-etl-job',
        script_location='s3://my-glue-scripts/glue_etl_script.py'
    )

    load_to_redshift = RedshiftDataOperator(
        task_id='load_to_redshift',
        database='dev',
        cluster_identifier='my-redshift-cluster',
        sql="""
            COPY customers_usa
            FROM 's3://my-datapipeline-bucket/processed/customers_usa/'
            IAM_ROLE 'arn:aws:iam::123456789012:role/MyRedshiftRole'
            FORMAT AS PARQUET;
        """,
        aws_conn_id='aws_default'
    )

    glue_etl >> load_to_redshift
