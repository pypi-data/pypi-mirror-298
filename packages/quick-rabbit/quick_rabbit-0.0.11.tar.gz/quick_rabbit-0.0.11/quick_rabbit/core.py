import simplejson as json
import os
from os import remove
import uuid
import pika


class RabbitMqClient:
    rabbit_channel = None
    props = None
    connection = None
    body = None

    def __init__(self, host: str, port: int, username: str, password: str, timer: int):
        """
        Initializes the RabbitMqClient class.

        This constructor sets up the connection parameters for the RabbitMQ client,
        including host, port, credentials, and a timer for the message handling.

        :param host: str
            The hostname or IP address of the RabbitMQ server.
        :param port: int
            The port number to connect to on the RabbitMQ server.
        :param username: str
            The username used for authentication with RabbitMQ.
        :param password: str
            The password used for authentication with RabbitMQ.
        :param timer: int
            The time duration (in seconds) to wait for message responses.
        """

        self.rabbit_host = host
        self.rabbit_port = port
        self.username = username
        self.password = password
        self.timer = timer

    def disconnect(self):
        """
        Closes the connection to the RabbitMQ server.

        This method safely closes the current connection to the RabbitMQ server
        to ensure no further communication can occur.
        """
        self.connection.close()

    def _connect(self):
        """
        Establishes a connection to the RabbitMQ server.

        This method sets up a connection to RabbitMQ using the provided credentials and connection parameters.
        It also creates a communication channel for interacting with RabbitMQ.

        """
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters(host=self.rabbit_host, port=int(self.rabbit_port),
                                               credentials=credentials, heartbeat=0)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.rabbit_channel = self.connection.channel()

    def declare_queue(self, list_queues: list):
        """
        Declares multiple RabbitMQ queues with specified properties.

        This method iterates over a list of queue names, declaring each one on the RabbitMQ server.
        Each queue is declared with a durable setting and a message time-to-live (TTL) based on the provided timer.

        :param list_queues: list
            A list of queue names to be declared.
        """
        for i in list_queues:
            self.rabbit_channel.queue_declare(queue=i, durable=True,
                                              arguments={'x-message-ttl': int(self.timer)})

    def _parse_response(self, res: dict, status: bool, route=""):
        """
        Handles the response based on the status and performs optional cleanup.

        This method processes the response by sending a success or failure message depending on the status.
        If the status is `True`, it sends a success response, clears temporary files if a route is provided,
        and prints "Send". If the status is `False`, it sends a failure response, clears temporary files,
        and prints "Canceled".

        :param res: dict
            The response data to be sent. Its type and structure depend on the context of the response.
        :param status: bool
            The status of the operation. If `True`, indicates a successful operation; if `False`, indicates failure.
        :param route: str, optional
            The path to temporary files to be cleared if provided. Defaults to an empty string, in which case no cleanup
            is performed.
        """
        if status:
            self.send_response(res=res, success=True)
            if route != "":
                clear_temp(route)
            self.clear_body()
            print("Send")
            return
        self.send_response(msg=res, success=False)
        clear_temp(route)
        self.clear_body()
        print("Canceled")

    def _recive(self, queue: str, list_queue: list):
        """
        Sets up and starts a consumer for the specified RabbitMQ queue.

        This method establishes a connection to RabbitMQ, declares the provided list of queues,
        and sets up a consumer to listen to the specified queue. It configures the consumer with
        quality-of-service settings and begins consuming messages from the queue.

        :param queue: str
            The name of the RabbitMQ queue to consume messages from.
        :param list_queue: list
            A list of queue names to be declared before starting the consumer. These queues are declared
            with the properties specified in the `declare_queue` method.
        """
        self._connect()
        self.declare_queue(list_queue)
        self.queue = queue
        self.rabbit_channel.basic_qos(prefetch_count=1)
        self.rabbit_channel.basic_consume(queue=queue, on_message_callback=self.callback, auto_ack=False)
        print("Info : start consumer")
        self.rabbit_channel.start_consuming()

    def callback(self, ch, method, properties, body):
        """
        Processes a message received from a RabbitMQ queue.

        This abstract method should be implemented by subclasses to define how messages
        are processed when received. It acknowledges the message, stores the message body,
        and stores the message properties.

        :param ch: pika.Channel
            The channel object used to communicate with RabbitMQ.
        :param method: pika.Basic.Deliver
            The delivery method information of the received message, including delivery tag.
        :param properties: pika.BasicProperties
            The properties of the received message, such as headers and message type.
        :param body: bytes
            The body of the received message, which will be deserialized into a Python object.
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.body = json.loads(body)
        self.props = properties

    def clear_body(self):
        self.body = None
        self.props = None

    def send_response(self, res=None, success=False, msg=None):
        """
        Sends a response message via RabbitMQ with the specified result, success status, and message.

        The response is published to the queue specified by the `reply_to` property of the original
        request message. The body of the response contains the correlation ID from the original message,
        the provided data, success status, and an optional message.

        :param res: The response data to be included in the message (default: None).
        :param success: A boolean indicating whether the operation was successful (default: False).
        :param msg: An optional message to be included, typically providing additional information or
                    context (default: None).

        """
        body = {'id': self.props.correlation_id,
                'data': res,
                "success": success,
                "message": msg}

        self.rabbit_channel.basic_publish(exchange='',
                                          routing_key=self.props.reply_to,
                                          properties=pika.BasicProperties(
                                              correlation_id=self.props.correlation_id,
                                          ),
                                          body=json.dumps(body, ignore_nan=True))

    def send_and_recive(self, queue, body):
        """
        Sends a message to the specified queue and waits for a response from the consumer.

        This method sends a message to the given RabbitMQ queue and creates an exclusive
        temporary callback queue to receive the response. The received response is then
        returned as a JSON object.

        :param queue: The name of the queue to which the message should be sent.
        :param body: The message payload to send, which will be serialized to JSON and sent to the queue.
                     It should be a dictionary that will include a unique `id` field (correlation ID).
        :return: The response message from the consumer as a JSON object.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self._connect()
            # We created an exclusive temporary queue for consumer response
            result = self.rabbit_channel.queue_declare(queue='', durable=True, auto_delete=True,
                                                       arguments={'x-message-ttl': int(self.timer)})
            callback_queue = result.method.queue
            self.rabbit_channel.queue_declare(queue=queue, durable=True,
                                              arguments={'x-message-ttl': int(self.timer)})
            cor_id = str(uuid.uuid4())
            body["id"] = cor_id
            self.rabbit_channel.basic_publish(exchange='',
                                              routing_key=queue,
                                              properties=pika.BasicProperties(
                                                  reply_to=callback_queue,
                                                  correlation_id=cor_id
                                              ),
                                              body=json.dumps(body, ignore_nan=True))

            method_frame = header_frame = body = None
            while method_frame is None:
                self.connection.process_data_events()
                method_frame, header_frame, body = self.rabbit_channel.basic_get(queue=callback_queue, auto_ack=True)
            return json.loads(body)
        except Exception as e:
            print("Error", e)
            self.connection.close()


def clear_temp(dir_name):
    """
     Removes a temporary directory or file.

    This function deletes the specified directory or file if the provided directory name
    is not an empty string.

    :param dir_name: str
        The name or path of the directory or file to be removed.
        If an empty string is passed, no action is taken.
    :return: None
        This function does not return a value.
    """
    if dir_name != "":
        remove(dir_name)
