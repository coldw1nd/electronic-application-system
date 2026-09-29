from datetime import date

import approvals
from documents import add_document


def test_get_approval_status():
    assert approvals.get_approval_status(-1) == (
        "Срок согласования истёк"
    )
    assert approvals.get_approval_status(1) == (
        "Срочное согласование"
    )
    assert approvals.get_approval_status(5) == (
        "Стандартное согласование"
    )


def test_create_approval():
    approval_list = []
    approval = approvals.create_approval(
        approval_list,
        1,
        "Петров П.П.",
        3,
    )
    assert approval is not None
    assert len(approval_list) == 1


def test_create_approval_low_level():
    approval_list = []
    approval = approvals.create_approval(
        approval_list,
        1,
        "Петров П.П.",
        1,
    )
    assert approval is None
    assert len(approval_list) == 0


def test_approve_document():
    document_list = []
    document = add_document(
        document_list,
        "Приказ",
        "Иванов И.И.",
        date(2026, 2, 1),
        7,
    )

    approval_list = []
    approval = approvals.create_approval(
        approval_list,
        document["id"],
        "Петров П.П.",
        3,
    )

    assert approval is not None

    result = approvals.approve_document(
        approval_list,
        document_list,
        approval["id"],
        date(2026, 2, 7),
    )

    assert result == "Документ согласован"
    assert approval["approved"] is True
