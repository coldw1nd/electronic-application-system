from datetime import date

from documents import add_document, find_documents, sort_documents


def test_add_document():
    document_list = []
    document = add_document(
        document_list,
        "Приказ",
        "Иванов И.И.",
        date(2026, 2, 1),
        7,
    )
    assert len(document_list) == 1
    assert document["due_date"] == "2026-02-08"


def test_find_documents():
    document_list = []
    add_document(
        document_list,
        "Приказ о командировке",
        "Иванов И.И.",
        date(2026, 2, 1),
        7,
    )
    assert len(find_documents(document_list, "приказ")) == 1
    assert len(find_documents(document_list, "договор")) == 0


def test_sort_documents():
    document_list = []
    add_document(
        document_list,
        "Б приказ",
        "Иванов И.И.",
        date(2026, 2, 1),
        7,
    )
    add_document(
        document_list,
        "А приказ",
        "Иванов И.И.",
        date(2026, 2, 1),
        7,
    )
    sorted_documents = sort_documents(document_list)
    assert sorted_documents[0]["title"] == "А приказ"
