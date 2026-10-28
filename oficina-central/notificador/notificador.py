import json
import os
import time

import pika
import pymysql

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_FILA = os.environ.get("RABBITMQ_FILA", "ordens_eventos")

DB = dict(
    host=os.environ.get("DB_HOST", "127.0.0.1"),
    port=int(os.environ.get("DB_PORT", "3307")),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "root"),
    database=os.environ.get("DB_NAME", "oficina_central"),
    charset="utf8mb4",
)

NOMES_STATUS = {
    "aberta": "Aberta",
    "em_andamento": "Em andamento",
    "aguardando_peca": "Aguardando peça",
    "pronto": "Pronto para retirada",
    "concluida": "Concluída",
}


def gravar_notificacao(ordem_id, status):
    mensagem = f"Ordem #{ordem_id:04d}: {NOMES_STATUS.get(status, status)}"
    conexao = pymysql.connect(**DB)
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO oficina_notificacao (ordem_id, mensagem, criada_em) "
                "VALUES (%s, %s, UTC_TIMESTAMP(6))",
                (ordem_id, mensagem),
            )
        conexao.commit()
    finally:
        conexao.close()


def ao_receber(canal, metodo, propriedades, corpo):
    try:
        evento = json.loads(corpo)
        gravar_notificacao(int(evento["ordem_id"]), evento["status"])
    except (ValueError, KeyError, pymysql.IntegrityError) as erro:
        # Mensagem inválida ou ordem que não existe mais: descarta.
        print(f"Mensagem descartada: {erro}")
        canal.basic_nack(delivery_tag=metodo.delivery_tag, requeue=False)
        return
    except pymysql.MySQLError as erro:
        # Banco fora do ar: devolve a mensagem pra fila e tenta depois.
        print(f"Banco indisponível, devolvendo à fila: {erro}")
        canal.basic_nack(delivery_tag=metodo.delivery_tag, requeue=True)
        time.sleep(3)
        return
    canal.basic_ack(delivery_tag=metodo.delivery_tag)
    print(f"Notificação gravada: {corpo.decode()}")


def main():
    while True:
        try:
            conexao = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            canal = conexao.channel()
            canal.queue_declare(queue=RABBITMQ_FILA, durable=True)
            canal.basic_qos(prefetch_count=1)
            canal.basic_consume(queue=RABBITMQ_FILA, on_message_callback=ao_receber)
            print("Notificador aguardando mensagens. Ctrl+C para sair.")
            canal.start_consuming()
        except pika.exceptions.AMQPError:
            print("RabbitMQ indisponível, tentando de novo em 5s...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Encerrando.")
            break


if __name__ == "__main__":
    main()