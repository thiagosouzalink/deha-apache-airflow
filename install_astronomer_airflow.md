
# Instalando o Airflow com Astronomer.io

## **1.Primeiro, certifique-se de ter o Docker instalado:**

```bash
sudo dnf install docker
sudo systemctl start docker
sudo systemctl enable docker
```

## **2.Instale o Astro CLI usando curl:**

```bash
curl -sSL install.astronomer.io | sudo bash -s
```

## **3.Verifique se a instalação foi bem-sucedida:**

```bash
astro version
```

## **4.Crie um novo projeto Airflow:**

```bash
mkdir meu-projeto-airflow
cd meu-projeto-airflow
astro dev init 
```

## **5.Inicie o Airflow localmente:**

```bash
astro dev start
```

Após executar estes comandos:

- O Airflow estará disponível em http://localhost:8080
- Username padrão: admin
- Senha padrão: admin

Observações importantes:

- Certifique-se que seu usuário está no grupo docker:

```bash
sudo usermod -aG docker $USER
```

- Pode ser necessário fazer logout e login novamente para que as alterações do grupo docker tenham efeito
- Se encontrar problemas de permissão, você pode precisar ajustar as permissões SELinux:

```bash
sudo setenforce 0
```

Para parar o ambiente quando necessário:

```bash
astro dev stop
```

A estrutura básica do projeto criado será:

```bash
.
├── .env
├── Dockerfile
├── dags/
├── include/
├── plugins/
└── requirements.txt
```

Você pode começar a adicionar suas DAGs no diretório dags/ e dependências adicionais no requirements.txt.
