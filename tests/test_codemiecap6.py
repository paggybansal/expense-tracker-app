import csv
import io
from datetime import date

import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    # models.DB_PATH is relative, so a fresh cwd gives each test its own database
    monkeypatch.chdir(tmp_path)
    import app as app_module
    import models

    models.init_db()
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def _add(amount, category, description, when=None):
    import models

    models.add_expense(amount, category, description, when or date.today().strftime("%Y-%m-%d"))


def _rows(resp):
    return list(csv.reader(io.StringIO(resp.get_data(as_text=True))))


def test_empty_export_returns_404_with_message(client):
    resp = client.get("/export/csv")
    assert resp.status_code == 404
    assert resp.get_data(as_text=True) == "No expense records available for export."


def test_export_header_attachment_and_rows(client):
    _add(30.0, "Food", "Lunch")
    resp = client.get("/export/csv")
    assert resp.status_code == 200
    assert "attachment" in resp.headers["Content-Disposition"]
    rows = _rows(resp)
    assert rows[0] == ["ID", "Title", "Category", "Amount", "Date"]
    assert rows[1][1:3] == ["Lunch", "Food"]


def test_export_honours_category_filter(client):
    _add(10.0, "Food", "Apple")
    _add(20.0, "Travel", "Bus")
    rows = _rows(client.get("/export/csv?category=Food"))
    assert [r[1] for r in rows[1:]] == ["Apple"]
    assert client.get("/export/csv?category=Utilities").status_code == 404


def test_export_honours_sort(client):
    _add(10.0, "Food", "Small")
    _add(50.0, "Food", "Big")
    rows = _rows(client.get("/export/csv?sort=amount_desc"))
    assert [r[1] for r in rows[1:]] == ["Big", "Small"]


@pytest.mark.parametrize("text", ["=1+1", "+1", "-1", "@x", "\tx", "\rx"])
def test_export_escapes_formula_cells(client, text):
    _add(5.0, text, text)
    row = _rows(client.get("/export/csv"))[1]
    assert row[1].startswith("'") and row[2].startswith("'")


def test_export_normalizes_dates(client):
    today = date.today()
    _add(5.0, "Food", "Mixed", today.strftime("%m/%d/%Y"))
    assert _rows(client.get("/export/csv"))[1][4] == today.strftime("%Y-%m-%d")


def test_export_escapes_text_in_amount_and_date(client):
    import models

    models.add_expense("=SUM(1)", "Food", "x", "=1+1")
    row = _rows(client.get("/export/csv"))[1]
    assert row[3] == "'=SUM(1)" and row[4] == "'=1+1"


def test_cards_count_mixed_date_formats(client):
    today = date.today()
    _add(40.0, "Food", "a", today.strftime("%Y/%m/%d"))
    _add(60.0, "Travel", "b", today.strftime("%m/%d/%Y"))
    html = client.get("/").get_data(as_text=True)
    assert "100.00" in html
    assert f"{100.0 / today.day:.2f}" in html


def test_cards_na_when_no_spend(client):
    html = client.get("/").get_data(as_text=True)
    assert "N/A" in html and "0.00" in html


def test_null_category_tie_does_not_crash(client):
    _add(100.0, None, "no category")
    _add(100.0, "Food", "food")
    resp = client.get("/")
    assert resp.status_code == 200


def test_null_category_alone_is_uncategorized(client):
    _add(100.0, None, "no category")
    assert "Uncategorized" in client.get("/").get_data(as_text=True)


def test_banner_matches_card_total(client):
    _add(1500.0, "Food", "big")
    html = client.get("/").get_data(as_text=True)
    assert "Monthly Budget Exceeded" in html and "1500.00" in html
