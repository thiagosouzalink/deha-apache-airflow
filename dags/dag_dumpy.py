from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator


# Definindo argumentos padrão
default_args = {
    "owner": "Thiago Souza",  # Nome do responsável pela DAG
    "depends_on_past": False,  # Não depende de DAGs anteriores
    "start_date": datetime.now() - timedelta(days=1),  # Data de inicio da DAG - 1 dia atrás
    "email_on_failure": False,  # Não envia email em caso de falha
    "email_on_retry": False,  # Não envia email em caso de retry
    "retries": 1,  # Número de retries
    "retry_delay": timedelta(minutes=5),  # Delay entre retries
}

# Definindo a DAG - Objeto que representa a DAG
dag = DAG(
    "dag_dummy",  # Nome da DAG
    default_args=default_args,  # Argumentos padrão
    description="A simple dummy DAG - Do nothing",  # Descrição da DAG
    schedule=timedelta(days=1)  # Intervalo de execução da DAG - A cada 1 dia
)

# Definindo o task de inicio da DAG
start = EmptyOperator(
    task_id="start",  # Identificador da task
    dag=dag  # Dag ao qual a task pertence
)

# Definindo a task de sleep da DAG
sleep = BashOperator(
    task_id="sleep",
    bash_command="sleep 10",
    dag=dag
)

# Definindo o task de fim da DAG
end = EmptyOperator(
    task_id="end",  # Identificador da task
    dag=dag  # Dag ao qual a task pertence
)

start >> sleep >> end