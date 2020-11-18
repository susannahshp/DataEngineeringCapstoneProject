from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class LoadToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 aws_credentials_id="",
                 redshift_conn_id="",
                 s3_bucket="",
                 s3_key="",
                 table="",
                 *args, **kwargs):

        super(LoadToRedshiftOperator, self).__init__(*args, **kwargs)

        self.aws_credentials_id = aws_credentials_id
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.table = table
       

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Clearing data from destination Redshift table")
        redshift_hook.run(f"DELETE FROM {self.table}")
        
        self.log.info("Copying data from S3 to Redshift")

        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key)

        copy_sql = """
            COPY {}
            FROM '{}'
            ACCESS_KEY_ID '{}'
            SECRET_ACCESS_KEY '{}'
            FORMAT AS PARQUET
            ;
        """
        formatted_sql = copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key
        )

        self.log.info(f'Executing COPY command from bucket s3://{self.s3_bucket}/{self.s3_key} to {self.table} in Redshift')
        redshift_hook.run(formatted_sql)
