import pytest

from jb_bootcamp.stack import Stack


def test_stack_push_and_pop() -> None:
    stack = Stack[int]()
    stack.push(1)
    stack.push(2)

    assert len(stack) == 2
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.is_empty()


def test_stack_peek_does_not_remove() -> None:
    stack = Stack(["a", "b"])

    assert stack.peek() == "b"
    assert len(stack) == 2


def test_stack_clear() -> None:
    stack = Stack(range(3))
    stack.clear()

    assert stack.is_empty()
    assert len(stack) == 0


def test_pop_from_empty_stack_raises() -> None:
    stack: Stack[int] = Stack()

    with pytest.raises(IndexError):
        stack.pop()


def test_peek_from_empty_stack_raises() -> None:
    stack: Stack[int] = Stack()

    with pytest.raises(IndexError):
        stack.peek()
