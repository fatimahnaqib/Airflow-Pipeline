from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments
default_args = {
    'owner': 'Fatimah Naqib',
    'start_date': days_ago(0),
    'email': ['fatimanaqib583@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
} 

# defining the DAG
dag = DAG(
    dag_id = 'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Project',
    schedule_interval=timedelta(days=1),
)

# define the tasks
unzip_data = BashOperator(
    task_id= 'unzip_data',
    bash_command= 'tar -xzvf /home/project/airflow/dags/finalassignment/tolldata.tgz'
    '-C /home/project/airflow/dags/finalassignment/staging',
    dag= dag,
)

extract_data_from_csv = BashOperator(
    task_id= 'extract_data_from_csv',
    bash_command= 'cut -d"," -f1-4 < /home/project/airflow/dags/finalassignment/staging/vehicle-data.csv >'
    ' /home/project/airflow/dags/finalassignment/staging/csv_data.csv',
    dag= dag,
)

extract_data_from_tsv = BashOperator(
    task_id= 'extract_data_from_tsv',
    bash_command= 'cut -f5-7 < /home/project/airflow/dags/finalassignment/staging/tollplaza-data.tsv >'
    '/home/project/airflow/dags/finalassignment/staging/tsv_data.csv',
    dag= dag,
)

extract_data_from_fixed_file = BashOperator(
    task_id= 'extract_data_from_fixed_file',
    bash_command= 'cut -c 59-68 < /home/project/airflow/dags/finalassignment/staging/payment-data.txt >'
    ' /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv',
    dag= dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command=(
        'paste -d"," /home/project/airflow/dags/finalassignment/staging/csv_data.csv '
        '/home/project/airflow/dags/finalassignment/staging/tsv_data.csv '
        '/home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv '
        '> /home/project/airflow/dags/finalassignment/staging/extracted_data.csv'
    ),
    dag=dag,
)

transform_data = BashOperator(
    task_id= 'transform_data',
    bash_command= 'tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/finalassignment/staging/extracted_data.csv',
    dag= dag,
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_file >> consolidate_data >> transform_data