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