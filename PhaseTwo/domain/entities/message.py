class Message:
    """
    Represents a message sent between client and server.
    """

    def __init__(self, content: str):
        self.content = content

    def is_close_command(self) -> bool:
        """
        Checks if the message is a command to close the connection.
        """
        return self.content.strip().lower() == "close"

    def __str__(self):
        return self.content
