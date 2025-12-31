from jb_bootcamp.node import Node


def test_build_and_iterate_nodes() -> None:
    head = Node.from_iterable([1, 2, 3])

    assert list(head) == [1, 2, 3]
    assert len(head) == 3


def test_append_extends_chain() -> None:
    head = Node(1)
    head.append(2)
    new_tail = head.append(3)

    assert new_tail.value == 3
    assert new_tail.next is None
    assert head.to_list() == [1, 2, 3]


def test_find_returns_matching_node() -> None:
    head = Node.from_iterable(["root", "middle", "leaf"])

    assert head.find("middle") is head.next
    assert head.find("missing") is None


def test_from_iterable_rejects_empty() -> None:
    try:
        Node.from_iterable([])
    except ValueError as exc:  # pragma: no cover - ValueError expected path
        assert "cannot build a Node" in str(exc)
    else:  # pragma: no cover - should not be reached
        raise AssertionError("ValueError not raised for empty iterable")
