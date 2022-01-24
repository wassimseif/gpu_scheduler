# Python stdlib
# Project Dependencies
import pytest

# Project Imports
from gpu_scheduler.models.command import Command


def test_working_init():
    cmd1 = Command(command_str="Hello World")
    assert cmd1.command == "Hello World"


def test_empty_init():
    with pytest.raises(TypeError):
        cmd1 = Command()


def test_equal_commands():
    cmd1 = Command(command_str="Hello World")
    cmd2 = Command(command_str="Hello World")
    assert cmd1 == cmd2


def test_not_equal_commands():
    cmd1 = Command(command_str="Hello1 World")
    cmd2 = Command(command_str="Hello World")
    assert cmd1 != cmd2


def test_ids_equal():
    cmd1 = Command(command_str="Hello World")
    cmd2 = Command(command_str="Hello World")
    assert cmd1.command == cmd2.command
    assert cmd1.uid == cmd2.uid


def test_ids_not_equal():
    cmd1 = Command(command_str="Hello World1")
    cmd2 = Command(command_str="Hello World")
    assert cmd1.command != cmd2.command
    assert cmd1.uid != cmd2.uid
