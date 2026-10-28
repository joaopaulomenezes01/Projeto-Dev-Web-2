# Projeto-Dev-Web-2 

# Oficina Central

Sistema web de ordens de serviço para oficina mecânica. O cliente deixa o carro, a oficina abre uma ordem, o mecânico atualiza o andamento (aberta, em andamento, aguardando peça, pronto para retirada, concluída) e o histórico fica registrado.

Projeto da disciplina Desenvolvimento de Sistemas Web II, IFPE Campus Paulista.

## O que tem

- CRUD completo de clientes, veículos, mecânicos e ordens de serviço, pela interface web
- Lista de ordens com busca (placa, cliente, descrição) e filtro por status
- Página da ordem com o histórico de status
- Publish-Subscribe com RabbitMQ: ao criar uma ordem ou mudar o status, o Django publica um evento na fila
- Notificador (microsserviço separado) que consome a fila e grava a notificação no MySQL
- Painel de notificações no sistema

## Tecnologias

Python, Django (MVT), HTML/CSS/JavaScript (Bootstrap), MySQL, RabbitMQ, Docker Compose, Git/GitHub.

## Estrutura

```
oficina-central/
  config/              configurações do Django
  oficina/             app principal (models, views, urls, templates, static, signals, mensageria)
  notificador/         microsserviço que consome a fila
  docker-compose.yml   MySQL e RabbitMQ
  requirements.txt     dependências do Python
  manage.py
```

## Como funciona o fluxo

1. O usuário cria uma ordem ou muda o status dela pela interface.
2. O Django grava no MySQL e registra uma linha no histórico.
3. Depois que a gravação é confirmada, o Django publica uma mensagem na fila `ordens_eventos` do RabbitMQ.
4. O Notificador, um processo separado, consome a mensagem e grava a notificação no MySQL.
5. A notificação aparece no painel **Notificações**.

## Como rodar

Precisa de Python 3.11+, Git e Docker Desktop aberto.

1. Clonar o repositório e entrar na pasta do projeto:

   ```
   git clone https://github.com/joaopaulomenezes01/Projeto-Dev-Web-2.git
   cd Projeto-Dev-Web-2/oficina-central
   ```

2. Criar e ativar o ambiente virtual e instalar as dependências:

   ```
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # Linux/Mac
   pip install -r requirements.txt
   ```

3. Subir o MySQL e o RabbitMQ:

   ```
   docker compose up -d
   ```

   Espere uns 20 segundos até o MySQL ficar pronto (`docker compose ps` mostra `healthy`).
   O painel do RabbitMQ fica em http://localhost:15672 (usuário e senha `guest`).

   O MySQL do Docker usa a porta **3307** no seu computador, pra não conflitar com um MySQL já instalado na 3306.

4. Criar as tabelas e iniciar o sistema:

   ```
   python manage.py migrate
   python manage.py runserver
   ```

5. Em outro terminal, com o ambiente virtual ativo, iniciar o Notificador:

   ```
   python notificador/notificador.py
   ```

6. Abrir http://127.0.0.1:8000, cadastrar cliente, veículo e mecânico, criar uma ordem e mudar o status dela. A notificação aparece em **Notificações**.

Opcional: `python manage.py createsuperuser` cria um usuário para entrar em http://127.0.0.1:8000/admin/.

## Configuração

Os padrões já funcionam com o `docker-compose.yml`. Para mudar, use variáveis de ambiente:

| Variável | Padrão |
| --- | --- |
| `DB_NAME` | `oficina_central` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | `root` |
| `DB_HOST` | `127.0.0.1` |
| `DB_PORT` | `3307` |
| `RABBITMQ_HOST` | `localhost` |
| `RABBITMQ_FILA` | `ordens_eventos` |

## Testes

```
python manage.py test
```

Os testes usam um banco temporário (o MySQL do Docker precisa estar de pé) e não precisam do RabbitMQ.

## Observações

- Se o RabbitMQ estiver fora do ar, a ordem é salva normalmente e só a notificação deixa de ser gerada.
- Se o Notificador estiver parado, as mensagens ficam na fila e viram notificações quando ele voltar.
- Excluir um cliente exclui também os veículos dele e as ordens ligadas a eles.