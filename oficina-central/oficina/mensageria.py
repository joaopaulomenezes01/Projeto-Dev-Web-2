import json
import logging

import pika
from django.conf import settings

logger = logging.getLogger(__name__)


def publicar_evento(ordem):
    corpo = json.dumps({"ordem_id": ordem.pk, "status": ordem.status})
    try:
        conexao = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        canal = conexao.channel()
        canal.queue_declare(queue=settings.RABBITMQ_FILA, durable=True)
        canal.basic_publish(
            exchange="",
            routing_key=settings.RABBITMQ_FILA,
            body=corpo,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        conexao.close()
    except (pika.exceptions.AMQPError, OSError):
        logger.warning("Não foi possível publicar o evento da ordem %s no RabbitMQ", ordem.pk)