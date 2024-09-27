# BotAPI

## Overview

The `BotAPI` class provides an interface for interacting with the Yandex Bot API. This class allows you to send messages (text, file, image) and manage incoming messages via polling. You can register message handlers using regular expressions and set up custom logic to process incoming messages.

## Features

- Send text messages to users via `chat_id` or `login`.
- Send file messages by specifying a file path.
- Send image messages with an image file path.
- Poll for new messages continuously.
- Decorate message handlers to process specific patterns using regular expressions.

## Installation

Ensure you have the necessary dependencies installed:

```bash
pip install httpx
```

## Usage

### Initialization

To initialize the bot, you need to pass the OAuth token:

```python
from bot_api import BotAPI

bot = BotAPI(token="your-oauth-token")
```

### Sending Messages

You can send different types of messages using the following methods:

- `send_text_message(message: Message, text: str)`
- `send_file_message(message: Message, file_path: str)`
- `send_image_message(message: Message, image_path: str)`

Example to send a text message:

```python
await bot.send_text_message(message, "Hello, World!")
```

### Handling Incoming Messages

You can register handlers for messages using the `@message_handler` decorator. The handler can process messages matching a specific pattern.

Example:

```python
@bot.message_handler(r'^/start')
async def start_handler(message):
    await bot.send_text_message(message, "Welcome to the bot!")
```

### Polling for Messages

To start polling for new messages, use the `start_polling` method:

```python
await bot.start_polling()
```

This will continuously poll for new messages and process them using registered handlers.

### Example Bot

Here is a complete example of setting up a simple bot that responds to the `/start` command:

```python
from bot_api import BotAPI

bot = BotAPI(token="your-oauth-token")

@bot.message_handler(r'^/start')
async def start_handler(message):
    await bot.send_text_message(message, "Welcome to the bot!")

async def main():
    await bot.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Methods

### `get_new_messages()`

Fetches new messages from the Yandex Bot API.

### `call_api_for_messages()`

Makes a request to the Yandex Bot API to retrieve updates and handles the polling offset.

### `send_text_message(message: Message, text: str)`

Sends a text message to the recipient.

### `send_file_message(message: Message, file_path: str)`

Sends a file message to the recipient.

### `send_image_message(message: Message, image_path: str)`

Sends an image message to the recipient.

### `get_recipient_info(message: Message)`

Determines whether to use the `login` or `chat_id` to send the message.

### `message_handler(pattern)`

A decorator to register a message handler for a specific pattern (regex or string).

### `process_message(message: Message)`

Processes an incoming message by matching it with a registered handler.

### `start_polling()`

Begins polling for new messages at the defined interval.

## License

This project is licensed under the MIT License.