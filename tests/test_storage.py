from pathlib import Path

from storage import load_data, save_data


def test_json_round_trip(tmp_path: Path) -> None:
    users, statuses, applications = load_data()
    save_data(users, statuses, applications, tmp_path)
    loaded_users, loaded_statuses, loaded_applications = load_data(tmp_path)
    assert len(loaded_users) == len(users)
    assert len(loaded_statuses) == len(statuses)
    assert len(loaded_applications) == len(applications)
    first = loaded_applications[0]
    assert first.applicant.full_name == users[0].full_name
    assert first.status.name == "На рассмотрении"
    assert all(doc.application_id == first.id for doc in first.documents)
