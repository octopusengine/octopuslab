from micropython import schedule

_subscribers = {}


def publisher(topic):
    def _publish(func):
        def _wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            publish(topic, value)
            return value

        return _wrapper

    return _publish


def publish(topic, value) -> None:
    if topic not in _subscribers:
        return

    for subscriber_func in _subscribers[topic]:
        schedule(subscriber_func, value)


def subscriber(topic):
    def _wrapper(func):
        try:
            _subscribers[topic].append(func)
        except KeyError:
            _subscribers[topic] = [func]

    return _wrapper
