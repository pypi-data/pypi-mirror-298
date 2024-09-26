import re
import asyncio
import httpx
from src.yandex_bot.schemas.message import PolingResponse, Message


class BotAPI:
    def __init__(
        self,
        token: str,
        base_url: str = "https://botapi.messenger.yandex.net/bot/v1",
        polling_interval: int = 1,
    ):
        self.base_url = base_url
        self.headers = {"Authorization": f"OAuth {token}"}
        self.handlers = {}

        self.polling_offset = 0
        self.polling_interval = polling_interval
        self.polling_endpoint = "/messages/getUpdates/?limit={limit}&offset={offset}"

        self.send_text_message_endpoint = "/messages/sendText"
        self.send_file_message_endpoint = "/messages/sendFile"
        self.send_image_message_endpoint = "/messages/sendImage"

    async def get_new_messages(self):
        response = await self.call_api_for_messages()
        new_messages = []

        for update in response.updates:
            new_messages.append(update)

        return new_messages

    async def call_api_for_messages(self) -> PolingResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url
                + self.polling_endpoint.format(limit=100, offset=self.polling_offset),
                headers=self.headers,
            )
            if response.status_code == 200:
                polling_response = PolingResponse.model_validate(response.json())
                update_ids = [update.update_id for update in polling_response.updates]
                if update_ids:
                    self.polling_offset = max(update_ids) + 1
                return polling_response
            else:
                print(response.status_code)

    async def send_text_message(self, message: Message, text: str):
        """
        Sends a text message. Automatically determines whether to send via login or chat_id.
        :param message: The received message object, which contains chat_id or login.
        :param text: The content of the message.
        """
        recipient, recipient_type = self.get_recipient_info(message)
        async with httpx.AsyncClient() as client:
            payload = {recipient_type: recipient, "text": text}
            response = await client.post(
                self.base_url + self.send_text_message_endpoint,
                headers=self.headers,
                json=payload,
            )
            if response.status_code != 200:
                print(f"Failed to send text message: {response.status_code}")

    async def send_file_message(self, message: Message, file_path: str):
        """
        Sends a file message. Automatically determines whether to send via login or chat_id.
        :param message: The received message object, which contains chat_id or login.
        :param file_path: The file path of the document to send.
        """
        recipient, recipient_type = self.get_recipient_info(message)
        async with httpx.AsyncClient() as client:
            files = {"document": open(file_path, "rb")}
            response = await client.post(
                self.base_url + self.send_file_message_endpoint,
                headers=self.headers,
                data={recipient_type: recipient},
                files=files,
            )
            if response.status_code != 200:
                print(f"Failed to send file message: {response.status_code}")

    async def send_image_message(self, message: Message, image_path: str):
        """
        Sends an image message. Automatically determines whether to send via login or chat_id.
        :param message: The received message object, which contains chat_id or login.
        :param image_path: The file path of the image to send.
        """
        recipient, recipient_type = self.get_recipient_info(message)
        async with httpx.AsyncClient() as client:
            files = {"image": open(image_path, "rb")}
            response = await client.post(
                self.base_url + self.send_image_message_endpoint,
                headers=self.headers,
                data={recipient_type: recipient},
                files=files,
            )
            if response.status_code != 200:
                print(f"Failed to send image message: {response.status_code}")

    def get_recipient_info(self, message: Message):
        """
        Determines whether to use the login or chat_id to send the message.
        :param message: The message object to extract recipient info.
        :return: A tuple of (recipient, recipient_type), where recipient_type is either 'login' or 'chat_id'.
        """
        if message.from_.login:
            return message.from_.login, "login"
        else:
            return message.chat.id, "chat_id"

    def message_handler(self, pattern):
        """
        Decorator to register a message handler for a specific pattern.
        :param pattern: A string or regex pattern to match message text.
        """

        def decorator(func):
            self.handlers[pattern] = func
            return func

        return decorator

    async def process_message(self, message: Message):
        for pattern, handler in self.handlers.items():
            if re.match(pattern, message.text):
                await handler(message)
                break

    async def start_polling(self):
        print("Polling for new messages...")

        while True:
            new_messages = await self.get_new_messages()

            if new_messages:
                for message in new_messages:
                    print(f"Received message: {message.text}")
                    await self.process_message(message)

            await asyncio.sleep(self.polling_interval)