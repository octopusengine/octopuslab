from micropython import schedule


class PubSub:
    def __init__(self) -> None:
        self._subscribers = {}

    def publish(self, name, *args, **kwargs) -> None:
        if name not in self._subscribers:
            return

        arg = (name, args, kwargs)

        for subscriber in self._subscribers[name]:
            schedule(subscriber, arg)

    def subscribe(self, name, subscriber) -> None:
        try:
            self._subscribers[name].append(subscriber)
        except KeyError:
            self._subscribers[name] = [subscriber]
