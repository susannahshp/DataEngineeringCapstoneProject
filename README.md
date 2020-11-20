# Project: Data Engineering Capstone Project



## Summary


The purpose of this Data Engineering Capstone Project is to ETL the data as a Data Engineer, so that the users(data scientists) can query the data efficiently and perform the analytics. 
The users wanted to perform the following four analytics:

1. **Figure out the state that has the most immigrants**
1. **Figure out the state that has the least immigrants**
1. **Figure out the state that has the most ratio of white people**
1. **Figure out the state that has the least ratio of white people**


To accomplish the purpose of this project, I made two stages. The first stage includes downloading the two source data(immigration data, demographics data) from the Customer's Repository(Udacity Workspace) to my **local computer**, and extracting and transforming the data using **Apache Spark** and loading the data to **Amazon S3**.
The second stage includes loading the star schema from **Amazon S3** to **Amazon Redshift** using **Apache Airflow**, and performing data quality check.




## Source Data

The following are two source data downloaded from the Udacity workspace.

**I94 Immigration Data** 


Columns | Description
------------ | -------------
cicid | ID that uniquely identify one record in the dataset
i94yr | 4 digit year
i94mon | Numeric month
i94cit | 3 digit code of source city for immigration (Born country)
i94res | 3 digit code of source country for immigration (Residence country)
i94port | Port addmitted through
arrdate | Arrival date in the USA
i94mode | Mode of transportation (1 = Air; 2 = Sea; 3 = Land; 9 = Not reported)
i94addr | State of arrival
depdate | Departure date
i94bir | Age of Respondent in Years
i94visa | Visa codes collapsed into three categories: (1 = Business; 2 = Pleasure; 3 = Student)
count | Used for summary statistics
gender | Gender
airline | Airline used to arrive in U.S.
fltno | Flight number of Airline used to arrive in U.S.
visatype | Class of admission legally admitting the non-immigrant to temporarily stay in U.S.
   

**U.S. City Demographic Data**


Columns | Description
------------ | -------------
City | Name of the city
State | US state of the city
Median Age | The median of the age of the population
Male Population | Number of the male population
Female Population | Number of the female population
Total Population | Number of the total population
Number of Veterans | Number of veterans living in the city
Foreign-born | Number of residents of the city that were not born in the city
Average Household Size | Average size of the houses in the city
State Code | Code of the state of the city
Race | Race class
Count | Number of individual of each race
   


## ETL data


### Data Dictionary 

There are the four tables made by extracting and transforming the data from the source data.
The first table is the fact table and the other three tables are dimension tables.

The following is the Data Dictionary of the four star-schema tables.

**Fact Table: fact_table** 

> I94 immigration data joined with the city demographic data on i94addr


Columns | Description
------------ | -------------
fact_id | ID that uniquely identify one record in the Fact Table
state_code | Code of the state
immigration_count | Count of immigration population by state
white | Count of white people by state
asian | Count of asian people by state
black | Count of black people by state
hispanic | Count of hispanic people by state
indian | Count of Indian people by state


**Dimension Table: dim_state_table**


Columns | Description
------------ | -------------
state_code | Code of the state
state | Full name of the state


**Dimension Table: dim_visa_table**


Columns | Description
------------ | -------------
state_code | Code of the state
B1 | Count of people that has B1 visa by state
B2 | Count of people that has B2 visa by state
CP | Count of people that has CP visa by state
CPL | Count of people that has CPL visa by state
E1 | Count of people that has E1 visa by state
E2 | Count of people that has E2 visa by state
F1 | Count of people that has F1 visa by state
F2 | Count of people that has F2 visa by state
GMT | Count of people that has GMT visa by state
I | Count of people that has I visa by state
I1 | Count of people that has I1 visa by state
M1 | Count of people that has M1 visa by state
M2 | Count of people that has M2 visa by state
SBP | Count of people that has SBP visa by state
WB | Count of people that has WB visa by state
WT | Count of people that has WT visa by state


**Dimension Table: dim_foreign_table**


Columns | Description
------------ | -------------
state_code | Code of the state
state_foreign_born | Count of people who were foreign born by state



The following is an image of the Star Schema Data Model.


![Imgae of Star Schema](https://github.com/susannahshp/DataEngineeringCapstoneProject/blob/main/star_schema.png)



### Data Architecture

The following is an image of the Data Architecture used for the project.

![Image of Data Architecture](https://github.com/susannahshp/DataEngineeringCapstoneProject/blob/main/data_architecture.png)


The following picture is the graph view of the Apache Airflow pipeline.


![Image of Airflow Graph](https://github.com/susannahshp/DataEngineeringCapstoneProject/blob/main/airflow_graph.png)







## How to run

### Configuration

#### Local Environment Configuration

The **Python** version used for the project is `Python 2.7.18`. You won't have to install Python 2.7 because you will have to set the python path to Python in Spark.

The **Java** version used for the project is `java-8-openjdk-amd64`. To install JDK 8 refer to this page: https://openjdk.java.net/install/.

The **Scala** version used for the project is `Scala version 2.11.12`.


#### Spark Configuration

The **Spark** version used for the project is `Spark version 2.4.7`. To install Apache Spark go to this url: https://spark.apache.org/downloads.html.
For the `Choose a package type` option select `Pre-built for Apache Hadoop 2.7` and download Spark.


The following lines will be the path settings. For the Linux operating system, add these lines to the `~/.bashrc` file.

```
export SPARK_HOME=/path/to/spark/home      ex) ~/Spark/spark-2.4.7-bin-hadoop2.7
export PATH=$PATH:/path/to/spark/home/bin  ex) ~/Spark/spark-2.4.7-bin-hadoop2.7/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
export PATH=$SPARK_HOME/python:$PATH
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/jre/bin
```

Add the following code in `$SPARK_HOME/conf/spark-defaults.conf.template`.

```
spark.jars.packages                com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.2,saurfang:spark-sas7bdat:2.0.0-s_2.11
```
Make sure the packages version numbers above match with jars in `~/.ivy2/jars`.


#### S3 Configuration

When you create a **S3 bucket** for the project, **turn off** the `Block public access(bucket settings)` in order to give permission to public to access the data.
Also set the Bucket policy like the following:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "*",
            "Resource": "arn:aws:s3:::my-bucket/*",
            "Condition": {
                "StringEquals": {
                    "s3:ExistingObjectTag/public": "yes"
                }
            }
        }
    ]
}
```

#### Redshift Configuration

When you create a **Redshift cluster** for the project, select `dc2.large` node type.
Set the **Database name** to `dev` and **Database port** to `5439` and **Master user name** to `awsuser` and enter your Master user password.
For the **Cluster permissions** add a pre-created IAM role. The IAM role has to have `AmazonS3FullAccess` policy attached.
Finally for the **Additional configurations** set **Enhanced VPC routing** to **Enabled**, and set **Publicly accessible** to **Yes**.
Set the other options to Default.


#### Airflow Configuration

To Quick Start Airflow:

```
# initialize the database
airflow initdb

# start the web server, default port is 8080
airflow webserver -p 8080

# start the scheduler
airflow scheduler

# visit localhost:8080 in the browser
```

From your airflow browser, go to **Admin menu** > **Connections** and create aws and redshift connections.
For the aws connection, set the **Conn Id** to `aws_credentials`, **Conn Type** to `Amazon Web Services`, **Login** to ACCESS KEY ID, **Password** to SECRET ACCESS KEY.

For the redshift connection, set the **Conn Id** to `redshift`, **Conn Type** to `Postgres`, **Host** to Endpoint of the Redshift Cluster excluding the port part, **Schema** to `dev`, **Login** to `awsuser`, **Password** to the password of your cluster, **Port** to `5439`.

Move the dag file under the `dags_folder` path, and plugins files under the `plugins_folder` path. The path information is inside the `airflow.cfg` file in your airflow home path.


### Steps to run the project

1. To run the Project, from conda py27 venv, run `jupyter-lab`. 
```
$ conda activate py27
$ jupyter-lab
```
You have to run all the cells from the `CapstoneProjectTemplate.ipynb` file in order to create the star-schema tables and perform the ETL process.

2. To create the tables in the Redshift cluster, run `create_tables.py` file which is inside the create_tables folder on your terminal.
The command should look like this: `python create_tables.py`

3. Finally, turn the `capstone_project_dag` DAG **ON** and trigger the DAG on airflow.


After the run your airflow tree view should look like this:

![Image of Tree View](https://github.com/susannahshp/DataEngineeringCapstoneProject/blob/main/airflow_tree_view.png)


Following is the Log of the `Run_Data_Quality_Checks` DataQualityOperator:

```
{data_quality.py:26} INFO - Starting data quality validation on fact_table table
{base_hook.py:89} INFO - Using connection to: id: redshift. Host: my-redshift-cluster.cp6jusobvffy.us-west-2.redshift.amazonaws.com, Port: 5439, Schema: dev, Login: awsuser, Password: XXXXXXXX, extra: None
{data_quality.py:35} INFO - Data quality on fact_table table check passed with 49 records
{data_quality.py:26} INFO - Starting data quality validation on dim_state_table table
{base_hook.py:89} INFO - Using connection to: id: redshift. Host: my-redshift-cluster.cp6jusobvffy.us-west-2.redshift.amazonaws.com, Port: 5439, Schema: dev, Login: awsuser, Password: XXXXXXXX, extra: None
{data_quality.py:35} INFO - Data quality on dim_state_table table check passed with 49 records
{data_quality.py:26} INFO - Starting data quality validation on dim_visa_table table
{base_hook.py:89} INFO - Using connection to: id: redshift. Host: my-redshift-cluster.cp6jusobvffy.us-west-2.redshift.amazonaws.com, Port: 5439, Schema: dev, Login: awsuser, Password: XXXXXXXX, extra: None
{data_quality.py:35} INFO - Data quality on dim_visa_table table check passed with 49 records
{data_quality.py:26} INFO - Starting data quality validation on dim_foreign_table table
{base_hook.py:89} INFO - Using connection to: id: redshift. Host: my-redshift-cluster.cp6jusobvffy.us-west-2.redshift.amazonaws.com, Port: 5439, Schema: dev, Login: awsuser, Password: XXXXXXXX, extra: None
{data_quality.py:35} INFO - Data quality on dim_foreign_table table check passed with 49 records
{taskinstance.py:1057} INFO - Marking task as SUCCESS.dag_id=capstone_project_dag, task_id=Run_Data_Quality_Checks, execution_date=20201116T035255, start_date=20201116T035614, end_date=20201116T035617
{local_task_job.py:102} INFO - Task exited with return code 0
```


## Complete Project Write Up


### Tools & Technologies

* **Python** : Python is used as the base programming language to perform the ETL of the data.

* **Spark** : Pyspark is used to process the Big data and load it to Amazon S3.

* **Amazon S3** : Amazon S3 is used for Storing processed outputs.

* **Airflow** : Airflow is used to load the star schema to Amazon Redshift and to perform data quality check.

* **Amazon Redshift** : Amazon Redshift is used as warehousing database.

* **Pandas** : Pandas is used to perform Data Analytics.


### Alternative approach to solve problem under different scenarios


#### The data was increased by 100x

The Redshift Cluster Node type `dc2.large` can handle storage of **160GB/node** and can have a maximum of **32 nodes(5.1 TB Total compressed storage)**.
So Redshift can easily handle the data increased by 100x.


#### The pipelines would be run on a daily basis by 7 am every day

To run the pipelines on a daily basis by **7 am every day**, add `schedule_interval='0 7 * * *'` to the DAG as the following.

```python
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
          description='Extract Load and Transform data from S3 to Redshift',
          schedule_interval='0 7 * * *'
        )
```


#### The database needed to be accessed by 100+ people

The maximum number of Redshift connections is **500** and **50** can run in parallel at a point in time, so 100+ people can easily connect to Redshift.

