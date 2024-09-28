"""Line reader."""

from collections import defaultdict
from wordly.status_codes import Status


class DictParser:
    def __init__(self, delimiter: bytes = b"\r\n"):
        self.line = b""
        self.mapping = defaultdict(str)
        self.DELIMITER = delimiter

    def _process_line(self, ending: str = ""):
        code = self.line[:3]

        if status := Status.by_value(code):
            self.mapping[status.name] += self.line[4:].decode() + ending
            self.part = status.name
        else:
            self.mapping[self.part] += self.line.decode() + ending

    def feed(self, stream: bytes):
        split = stream.split(self.DELIMITER, 1)
        while len(split) > 1:
            old, new = split
            self.line += old
            self._process_line("\n")
            self.line = b""
            split = new.split(self.DELIMITER, 1)

        if line := split[0]:
            self.line += line
            self._process_line()
            self.line = b""
