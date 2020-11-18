from datetime import datetime
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from operators import (LoadToRedshiftOperator, DataQualityOperator)

default_args = {
    'owner': 'Susannah Park',
    'start_date': datetime.now(),
    'depends_on_past': False,
    'email_on_retry': False,
    'email_on_failure': False,
    'catchup': False
}

dag_name = 'capstone_project_dag' 

dag = DAG(dag_name,
          default_args=default_args,
          description='Extract Load and Transform data from S3 to Redshift'
        )

start_operator = DummyOperator(task_id='Begin_Execution', dag=dag)

load_fact_table = LoadToRedshiftOperator(
    task_id='Load_Fact_Table',
    aws_credentials_id='aws_credentials',
    redshift_conn_id='redshift',
    s3_bucket='my-bucket',
    s3_key='fact_table',
    table='fact_table',
    mode='truncate',
    dag=dag
)

load_dim_state_table = LoadToRedshiftOperator(
    task_id='Load_Dim_State_Table',
    aws_credentials_id='aws_credentials',
    redshift_conn_id='redshift',
    s3_bucket='my-bucket',
    s3_key='dim_state_table',
    table='dim_state_table',
    mode='truncate',
    dag=dag
)

load_dim_visa_table = LoadToRedshiftOperator(
    task_id='Load_Dim_Visa_Table',
    aws_credentials_id='aws_credentials',
    redshift_conn_id='redshift',
    s3_bucket='my-bucket',
    s3_key='dim_visa_table',
    table='dim_visa_table',
    mode='truncate',
    dag=dag
)

load_dim_foreign_table = LoadToRedshiftOperator(
    task_id='Load_Dim_Foreign_Table',
    aws_credentials_id='aws_credentials',
    redshift_conn_id='redshift',
    s3_bucket='my-bucket',
    s3_key='dim_foreign_table',
    table='dim_foreign_table',
    mode='truncate',
    dag=dag
)



run_quality_checks = DataQualityOperator(
    task_id='Run_Data_Quality_Checks',
    redshift_conn_id='redshift',
    tables=['fact_table','dim_state_table','dim_visa_table','dim_foreign_table'],
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_Execution',  dag=dag)



start_operator >> load_fact_table

load_fact_table >> [load_dim_state_table, load_dim_visa_table, load_dim_foreign_table]

[load_dim_state_table, load_dim_visa_table, load_dim_foreign_table] >> run_quality_checks

run_quality_checks >> end_operator