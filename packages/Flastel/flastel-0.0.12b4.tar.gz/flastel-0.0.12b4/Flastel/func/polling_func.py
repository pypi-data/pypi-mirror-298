import aiohttp
import asyncio
import logging

def keyboard_create(callback=None, reply_keyboard=None):
    reply_markup = None

    if callback:
        reply_markup = {"inline_keyboard": []}
        for key, value in callback.items():
            if value.startswith("http://") or value.startswith("https://"):
                reply_markup["inline_keyboard"].append([{"text": key, "url": value}])
            else:
                reply_markup["inline_keyboard"].append([{"text": key, "callback_data": value}])
    elif reply_keyboard:
        reply_markup = {
            "keyboard": [[{"text": button} for button in row] for row in reply_keyboard],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }

    return reply_markup

class TelegramPollingBot:
    def __init__(self, bot_token):  # Fixed init method name
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.commands = {}
        self.param_commands = {}

    async def get_updates(self, offset=None):
        url = f"{self.api_url}getUpdates"
        params = {"offset": offset, "timeout": 60}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("result", [])
                return []

    async def send_message(self, chat_id, text, parse_mode=None, callback=None, reply_keyboard=None):
        url = f"{self.api_url}sendMessage"
        reply_markup = keyboard_create(callback, reply_keyboard)
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("result", {})
                return None

    async def run_polling(self):
        offset = None
        while True:
            updates = await self.get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                message_data = update.get("message")
                if message_data:
                    message = TelegramMessage(message_data)
                    await self.process_message(message)
            await asyncio.sleep(1)

    async def process_message(self, message):
        text = message.text

        if text.startswith("/"):
            parts = text.split()
            command = parts[0].lower()
            params = parts[1:] if len(parts) > 1 else []

            if command in self.param_commands:
                handler, allowed_params = self.param_commands[command]
                if params and any(param in allowed_params for param in params):
                    await handler(message, params)
                    return

            if command in self.commands:
                await self.commands[command](message)
                
    def command(self, commands, caps_ignore=True):
        def decorator(func):
            for command in commands:
                if caps_ignore:
                    self.commands[command.lower()] = func
                    self.commands[command.upper()] = func
                else:
                    self.commands[command] = func
            return func
        return decorator

    def command_with_params(self, commands, params, caps_ignore=True):
        def decorator(func):
            for command in commands:
                if caps_ignore:
                    self.param_commands[command.lower()] = (func, params)
                    self.param_commands[command.upper()] = (func, params)
                else:
                    self.param_commands[command] = (func, params)
            return func
        return decorator

class TelegramMessage:
    def __init__(self, message_data):  # Fixed init method name
        self.chat_id = message_data["chat"]["id"]
        self.text = message_data.get("text", "")
        self.from_user = TelegramUser(message_data["from"])

class TelegramUser:
    def __init__(self, user_data):  # Fixed init method name
        self.user_id = user_data["id"]
        self.first_name = user_data.get("first_name", "")
        self.last_name = user_data.get("last_name", "")
        self.all_name = f"{self.first_name} {self.last_name}".strip()
