import os

from tc_messageBroker import RabbitMQ


def test_rabbitmq_env_variables():
    """
    test if the environment variables are loaded correctly
    """
    broker_url = os.getenv("RABBIT_HOST")
    port = os.getenv("RABBIT_PORT")
    username = os.getenv("RABBIT_USER")
    password = os.getenv("RABBIT_PASSWORD")

    assert broker_url is not None
    assert port is not None
    assert username is not None
    assert password is not None


def test_tc_message_broker_connection():
    """
    test connecting to rabbitMQ and defining a queue for that
    """
    broker_url = os.getenv("RABBIT_HOST")
    port = os.getenv("RABBIT_PORT")
    username = os.getenv("RABBIT_USER")
    password = os.getenv("RABBIT_PASSWORD")

    messageBroker = RabbitMQ(
        broker_url=broker_url, port=port, username=username, password=password
    )

    _ = messageBroker.connect(queue_name="test_queue")
