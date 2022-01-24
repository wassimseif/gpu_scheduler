# Python stdlib
from typing import Dict
from uuid import uuid4
from hashlib import sha256

# Project Dependencies

# Project Imports


class Command:
    uid: str
    command: str

    def __init__(self, command_str: str, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.command = command_str
        self.uid = sha256(command_str.encode("utf-8")).hexdigest()

    def __eq__(self, other):
        return self.command == other.command and self.uid == other.uid

    def __str__(self):
        return f"{self.command} - {self.uid}"

    def __repr__(self):
        return f"{self.command} - {self.uid}"

    def to_json(self) -> Dict:
        return {"uid": self.uid, "command": self.command}


if __name__ == "__main__":
    cmd1 = Command(command_str="A")
