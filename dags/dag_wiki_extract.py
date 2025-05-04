from datetime import datetime, timedelta
import re

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
import requests


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
    "dag_wiki_extract",  # Nome da DAG
    default_args=default_args,  # Argumentos padrão
    description="Extract data from Wikipedia",  # Descrição da DAG
    schedule=timedelta(days=1)  # Intervalo de execução da DAG - A cada 1 dia
)

ENDPOINT = "https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"

def extract_html():
    response = requests.get(ENDPOINT)
    with open("/tmp/wikipedia_page.html", "w") as file_:
        file_.write(response.text)
        
def extract_links_from_html():
    with open("/tmp/wikipedia_page.html", "r") as file_:
        content = file_.read()
        links = re.findall(r'<a href="([^"]+)">', content)  # Encontra todos os links da página
        print(links)

# Definindo o task de inicio da DAG
start = EmptyOperator(
    task_id="start",  # Identificador da task
    dag=dag  # Dag ao qual a task pertence
)

# Definindo o task de fim da DAG
end = EmptyOperator(
    task_id="end",  # Identificador da task
    dag=dag  # Dag ao qual a task pertence
)

# Extrair HTML da página principal do Wikipedia
# extract_html = BashOperator(
#     task_id="extract_html",
#     bash_command=f"curl -o /tmp/wikipedia_page.html {ENDPOINT}",
#     dag=dag
# )

extract_html = PythonOperator(
    task_id="extract_html",
    python_callable=extract_html,
    dag=dag
)

# Exibir links
extract_links = PythonOperator(
    task_id="extract_links",
    python_callable=extract_links_from_html,
    dag=dag
)

# # Imprimindo o contaúdo do arquivo html
# print_html = BashOperator(
#     task_id="print_html",
#     bash_command=f"cat /tmp/wikipedia_page.html",
#     dag=dag
# )

start >> extract_html >> extract_links >> end