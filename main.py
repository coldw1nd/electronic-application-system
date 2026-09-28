from datetime import date, timedelta


def register_document(title, author, created_at, days_for_approval):
    due_date = created_at + timedelta(days=days_for_approval)
    return (
        f"Документ '{title}' создан автором {author}. "
        f"Срок согласования до {due_date}"
    )


def can_approve(is_ready, days_left):
    if is_ready and days_left >= 0:
        return True
    return False


def get_approval_status(days_left):
    if days_left < 0:
        return "Срок согласования истёк"
    elif days_left <= 2:
        return "Срочное согласование"
    return "Стандартное согласование"


def add_comment(author, text):
    return f"{author}: {text}"


def can_assign_approver(approver_level):
    if approver_level >= 2:
        return True
    return False


def main():
    document_title = "Приказ о командировке"
    author = "Иванов И.И."
    approver = "Петров П.П."
    created_at = date(2026, 2, 1)
    days_for_approval = int("7")
    approver_level = int("3")
    today = date(2026, 2, 7)
    is_document_ready = True

    due_date = created_at + timedelta(days=days_for_approval)
    days_left = (today - due_date).days

    print(
        register_document(
            document_title,
            author,
            created_at,
            days_for_approval
        )
    )
    print(f"Дата согласования: {due_date}")
    print(f"Осталось дней: {days_left}")
    print(f"Статус: {get_approval_status(days_left)}")
    print(f"Можно согласовать: {can_approve(is_document_ready, days_left)}")
    print(f"Согласующий назначен: {can_assign_approver(approver_level)}")
    print(add_comment(approver, "Согласовано без замечаний"))


if __name__ == "__main__":
    main()
