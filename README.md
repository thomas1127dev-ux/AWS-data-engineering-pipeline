# AWS Data Engineering Pipeline

This repository contains an advanced AWS Data Engineering pipeline using S3, Lambda, MWAA (Apache Airflow), Glue, and Redshift.

## Project Overview

- **S3**: Stores raw and processed data
- **Lambda**: Triggers Airflow DAG on new file upload
- **MWAA/Airflow**: Orchestrates ETL and data load tasks
- **Glue**: Cleans and transforms raw data
- **Redshift**: Stores final analytics-ready data

## File Structure

- `lambda/lambda_trigger_airflow.py` — Lambda function to trigger Airflow DAG
- `glue/glue_etl_script.py` — AWS Glue ETL script
- `airflow/data_pipeline.py` — Airflow DAG definition
- `sql/create_redshift_table.sql` — SQL to create Redshift table
- `config/s3_event_notification.json` — S3 bucket event notification for Lambda
- `config/iam_role_policy.json` — IAM policy for necessary permissions

## Setup Instructions

1. **Create S3 Bucket**
   - Upload your raw CSV data (e.g., `customers.csv`).

2. **Configure S3 Event Notification**
   - Use `config/s3_event_notification.json` to trigger Lambda on new CSV uploads.

3. **Deploy Lambda Function**
   - Use `lambda/lambda_trigger_airflow.py`.
   - Set environment variables for MWAA environment and DAG name.

4. **Set IAM Roles**
   - Use `config/iam_role_policy.json` for Lambda, Glue, and Redshift.

5. **Create Glue Job**
   - Use `glue/glue_etl_script.py` as your Glue ETL script.
   - Set input and output S3 paths.

6. **Set Up MWAA/Airflow**
   - Deploy `airflow/data_pipeline.py` in your Airflow environment.
   - Ensure Glue and Redshift operators are available.

7. **Create Redshift Table**
   - Run `sql/create_redshift_table.sql` in your Redshift cluster.

## Usage

- Upload a CSV file to the S3 bucket.
- The S3 event triggers Lambda, which starts the Airflow DAG.
- The DAG runs Glue ETL and loads processed data into Redshift.

## License

MIT