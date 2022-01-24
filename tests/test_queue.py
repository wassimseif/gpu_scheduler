# Python stdlib
from copy import copy

# Project Dependencies
import pytest

# Project Imports
from gpu_scheduler.models.commandqueue import CommandQueue
from gpu_scheduler.models.command import Command


def test_empty():
    q = CommandQueue()
    assert q.is_empty()


def test_not_empty():
    q = CommandQueue()
    cmd = Command("python")
    q.enqueue(cmd=cmd)
    assert not q.is_empty()


def test_removing_last_elm():
    q = CommandQueue()
    cmd = Command("python")
    q.enqueue(cmd=cmd)
    a = q.dequeue()
    assert q.is_empty()


def test_removing_elm_by_equal():
    q = CommandQueue()
    cmd1 = Command("python")
    cmd2 = Command("python")
    q.enqueue(cmd=cmd1)
    q.remove_elm(cmd2)
    assert q.is_empty()


def test_elm_exists():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd=cmd1)
    assert q.elm_exists(cmd1)


def test_not_elm_exists():
    q = CommandQueue()
    cmd1 = Command("python")
    cmd2 = Command("python2")
    q.enqueue(cmd=cmd1)
    assert not q.elm_exists(cmd2)


def test_front_rear_same_elm():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd1)
    assert q.front() == q.rear() == cmd1


def test_no_duplicates():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd1)

    assert not q.enqueue(cmd1)
    assert q.size() == 1


def test_two_diff_elms():
    q = CommandQueue()
    cmd1 = Command("python")
    cmd2 = Command("python2")
    q.enqueue(cmd1)

    assert q.enqueue(cmd2)
    assert q.size() == 2


def test_loop_inserts_same():
    q = CommandQueue()
    for i in range(10):
        cmd1 = Command("python")
        q.enqueue(cmd1)
    assert q.size() == 1
    assert q.front() == q.rear() == cmd1


def test_loop_inserts_diff():
    n = 10
    q = CommandQueue()
    for i in range(n):
        cmd = Command(f"python {i}")
        q.enqueue(cmd)
    assert q.size() == n


def test_inserting_not_command():

    q = CommandQueue()
    with pytest.raises(AssertionError):
        q.enqueue(1)


def test_copy_empty():
    q = CommandQueue()
    nq = copy(q)
    assert nq.is_empty()
    assert nq.size() == q.size()


def test_copy_one_cmd():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd1)
    nq = copy(q)
    assert not nq.is_empty()
    assert nq.size() == q.size()
    assert nq.size() == 1


def test_copy_then_insert_first():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd1)
    nq = copy(q)
    cmd2 = Command("python2")
    q.enqueue(cmd2)
    assert q.size() == 2
    assert nq.size() == 1


def test_copy_then_insert_second():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd1)
    nq = copy(q)
    cmd2 = Command("python2")
    nq.enqueue(cmd2)

    assert nq.size() == 2
    assert q.size() == 1


def test_remove_elm_with_uid():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd1)
    t = cmd1.uid
    assert q.remove_elm_uid(t)
    assert q.is_empty()


def test_fail_remove_elm_with_uid():
    q = CommandQueue()
    cmd1 = Command("python")
    q.enqueue(cmd1)
    t = cmd1.uid + "12"
    assert not q.remove_elm_uid(t)
    assert not q.is_empty()
