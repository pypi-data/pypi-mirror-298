from .base import AbstractLogger
import pickle


class LogMsg:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self) -> str:
        return f"{self.name}: {self.content}"

    def __repr__(self) -> str:
        return f"LogMsg({self.name}, {self.content})"


class LogBlock:
    def __init__(self, template):
        self.content = []
        self._looper = None
        for item in template:
            if isinstance(item, str):
                self.content.append(LogMsg(item, None))
            elif isinstance(item, list):
                self.content.append(LogBlock(item))
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.content[key]
        elif isinstance(key, str):
            for item in self.content:
                if isinstance(item, LogMsg) and item.name == key:
                    return item.content
                elif isinstance(item, LogBlock):
                    return item[key]
            raise KeyError(f"Key {key} not found in LogBlock")
    def _loop_over(self):
        for item in self.content:
            if isinstance(item, LogMsg):
                yield item
            elif isinstance(item, LogBlock):
                yield from item._loop_over()
            else:
                raise TypeError(f"Invalid type {type(item)} in LogBlock")

    def __iter__(self):
        self._looper = self._loop_over()
        return self

    def __next__(self):
        return next(self._looper)#type: ignore


class StaticLogger(AbstractLogger):
    """
    A quite simple but structured logger.

    Example:
        logger = StaticLogger([
            "layer_idx",
            ["x","y"] * 5,
            "post_scores",
            ...
        ], print)#print for example
    And when you use it:
        logger.log("layer_idx", 0)
        for i in range(5):
            logger.log("x", 1)
            ...
    output_func will always receive a structured LogBlock object.
    Which allows you to easily extract the information you need.

    This logger always assume you log as the order you defined and no branches.
    """

    def __init__(self, template:list, output_func):
        self.template = template
        self._block = LogBlock(template)
        self.output_func = output_func
        self._iterator = iter(self._block)
        self._next_msg = next(self._iterator)

    def log(self, key, value):
        msg = self._next_msg
        if msg.name == key:
            msg.content = value
        else:
            raise ValueError(f"Invalid key {key} for static logger which expects {msg}")
        try:
            msg = next(self._iterator)
        except StopIteration:
            self._flushout()
            self._iterator = iter(self._block)
            msg = next(self._iterator)
        self._next_msg = msg

    def _flushout(self):
        self._block._looper = None
        self.output_func(self._block)


class PickleTo:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, "wb")
    def __call__(self, block):
        pickle.dump(block, self.file)
        self.file.flush()
    def __del__(self):
        self.file.close()
