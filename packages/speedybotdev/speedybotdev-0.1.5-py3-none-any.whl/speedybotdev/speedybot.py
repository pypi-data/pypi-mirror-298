from typing import Callable, Dict, List, Optional, TypedDict, Union
from enum import Enum


class EventType(Enum):
    TEXT = "text"
    FILE = "file"
    CARD = "card"


class SpeedyBot:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.middlewares: List[Callable] = []
        self.handlers = {
            EventType.TEXT: [],
            EventType.FILE: [],
            EventType.CARD: []
        }

    def add_step(self, handler: Callable, event_type: EventType) -> None:
        """Adds a handler function to the appropriate event list."""
        self.handlers[event_type].append(handler)

    def on_text(self, func: Callable) -> Callable:
        """Decorator to add a text handler."""
        self.add_step(func, EventType.TEXT)
        return func

    def on_file(self, condition: Callable[[Dict], bool] = lambda f: True) -> Callable:
        """Decorator to add a file handler with an optional condition."""
        def decorator(func: Callable) -> Callable:
            def wrapper(ctx, file_data):
                if condition(file_data):
                    return func(ctx, file_data)
            self.add_step(wrapper, EventType.FILE)
            return wrapper
        return decorator

    def on_card(self, func: Callable) -> Callable:
        """Decorator to add a card handler."""
        self.add_step(func, EventType.CARD)
        return func

    def run_event(self, event_type: EventType, ctx, **kwargs):
        """Run the registered handlers for a specific event type."""
        for handler in self.handlers[event_type]:
            result = handler(ctx, **kwargs)
            if result is False:
                break



# bot = SpeedyBot(token="your-token")

# @bot.on_text
# def handle_text(ctx, text: str):
#     print(f"Handling text: {text}")
#     return True

# @bot.on_file(lambda file: file.get("extension") == "pdf")
# def handle_file(ctx, file: Dict):
#     print(f"Handling file: {file['name']} with extension {file['extension']}")
#     return True

# @bot.on_card
# def handle_card(ctx, data: Dict, file: str):
#     file.capitalize
#     print(f"Handling card data: {data}")
#     return True
