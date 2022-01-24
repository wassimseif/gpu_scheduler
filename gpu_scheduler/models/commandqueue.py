# Python stdlib
from typing import List

# Project Dependencies
# Project Imports
from gpu_scheduler.models.command import Command


class CommandQueue:
    def __init__(self):
        """
        Initializing Queue.
        """
        self.storage: List[Command] = []

    def is_empty(self) -> bool:
        return True if len(self.storage) == 0 else False

    def size(self) -> int:
        return len(self.storage)

    def front(self) -> Command:
        return self.storage[-1]

    def rear(self) -> Command:
        return self.storage[0]

    def enqueue(self, cmd: Command) -> bool:
        assert isinstance(cmd, Command)
        if self.elm_exists(cmd):
            return False
        self.storage.insert(0, cmd)
        return True

    def dequeue(self) -> Command:
        return self.storage.pop()

    def remove_elm(self, command: Command) -> bool:
        if not self.elm_exists(command):
            return False
        for i, c in enumerate(self.storage):
            if c == command:
                del self.storage[i]
                return True
        return False

    def remove_elm_uid(self, uid: str) -> bool:
        for i, c in enumerate(self.storage):
            if c.uid == uid:
                del self.storage[i]
                return True
        return False

    def elm_exists(self, command: Command) -> bool:
        return command in self.storage

    def __copy__(self):
        newq = CommandQueue()
        newq.storage = self.storage.copy()
        return newq


if __name__ == "__main__":
    q = CommandQueue()
    cmd1 = Command("python")
    t = cmd1.uid
    assert q.remove_elm_uid(t)
