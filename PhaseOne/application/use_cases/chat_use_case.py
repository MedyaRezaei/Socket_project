from domain.entities.message import Message

class ChatUseCase:
    def process_message(self, message: Message) -> str:
        if message.is_close_command():
            return "Closing connection."
        return "Hello client"
