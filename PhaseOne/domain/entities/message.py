class Message:
    def __init__(self, content: str):
        self.content = content

    def is_close_command(self) -> bool:
        return self.content.lower() == "close"
