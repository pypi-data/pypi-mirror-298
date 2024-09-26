from .core import RabbitMqClient


def get_data(host: str, port: int, username: str, password: str, timer: int, cmd, queue, data=None):
    """
        Sends a command to a specific RabbitMQ queue and retrieves the response.

        This function connects to a RabbitMQ server using the provided credentials,
        sends a message to a specific queue, and optionally includes additional data.
        After sending the message, it waits for a response and then disconnects from the server.

        :param host: str
            The RabbitMQ server address (can be localhost, a Docker network, or any remote host).
        :param port: int
            The RabbitMQ server port to connect to.
        :param username: str
            Username for authentication with RabbitMQ.
        :param password: str
            Password for authentication with RabbitMQ.
        :param timer: int
            Duration (in seconds) for which the connection should wait for a response.
        :param cmd: str
            Command to be sent in the message to the queue.
        :param queue: str
            The name of the RabbitMQ queue to send the message to.
        :param data: optional
            Additional data to include in the message. If not provided, only the command will be sent.
        :return: dict
            The response received from the RabbitMQ queue.
        """

    msj = {'pattern': {"cmd": cmd}}
    if data is not None:
        msj = {'pattern': {"cmd": cmd}, 'data': data}

    sr = RabbitMqClient(host, port, username, password, timer)
    result = sr.send_and_recive(queue, msj)
    sr.disconnect()
    return result


def consumer(host: str, port: int, username: str, password: str, timer: int, queue: str, constructor):
    """
        Starts a consumer that listens to a specific RabbitMQ queue.

        This function initializes a consumer that will keep listening to the provided RabbitMQ queue.
        It takes a constructor function that should be used to create and redefine parts of the
        `RabbitMqClient` object for custom behavior during message handling.

        :param list_queues: list
            A list of queues to be declared in RabbitMQ.
        :param host: str
            The RabbitMQ server address (can be localhost, a Docker network, or any remote host).
        :param port: int
            The RabbitMQ server port to connect to.
        :param username: str
            Username for authentication with RabbitMQ.
        :param password: str
            Password for authentication with RabbitMQ.
        :param timer: int
            Duration (in seconds) for which the connection should wait for a response.
        :param queue: str
            The name of the RabbitMQ queue to listen to.
        :param constructor: callable
            A constructor function used to instantiate an object that customizes
            the behavior of the RabbitMqClient. This function should return an object
            that implements a `recive` method to handle incoming messages.
        :return: None
            This function does not return a value.
    """

    cg = constructor(host, port, username, password, timer)
    cg.recive(queue, [queue])
