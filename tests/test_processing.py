import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    ("state", "expected_ids"),
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(operations, state, expected_ids):
    result = filter_by_state(operations, state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default(operations):
    result = filter_by_state(operations)
    assert [item["id"] for item in result] == [41428829, 939719570]


def test_sort_by_date_newest_first(operations):
    result = sort_by_date(operations)
    assert [item["id"] for item in result] == [
        41428829,
        615064591,
        594226727,
        939719570,
    ]


def test_sort_by_date_oldest_first(operations):
    result = sort_by_date(operations, is_reversed=False)
    assert [item["id"] for item in result] == [
        939719570,
        594226727,
        615064591,
        41428829,
    ]


def test_sort_by_date_keeps_order_for_equal_dates(same_date_operations):
    result = sort_by_date(same_date_operations)
    assert [item["id"] for item in result] == ["first", "second"]


def test_sort_by_date_accepts_date_without_time():
    items = [
        {"id": "date_only", "date": "2024-03-11"},
        {"id": "timestamp", "date": "2024-03-11T12:00:00"},
    ]

    result = sort_by_date(items)
    assert [item["id"] for item in result] == ["timestamp", "date_only"]


@pytest.mark.parametrize("date", ["", "не дата", "2024-13-40"])
def test_sort_by_date_rejects_invalid_date(date):
    with pytest.raises(ValueError):
        sort_by_date([{"date": date}])
