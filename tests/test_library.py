import re
import requests

host = "http://localhost:5042"
email = 'princess.bubblegum@candykingdom.ooo'
title = 'The Enchiridion'

def test_list_has_no_reservations():
    resp = requests.get(f"{host}/request")

    assert resp.status_code == 200
    assert resp.json() == []


def test_make_reservation():
    resp = requests.post(f"{host}/request", data={
        'email': email,
        'title': title
    })
    reservation = resp.json()

    assert resp.status_code == 200
    assert reservation['reservation_id'] > 0
    assert reservation['title'] == title
    assert reservation['email'] == email
    assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
            reservation['timestamp'])


def test_list_has_one_reservation():
    resp = requests.get(f"{host}/request")
    reservations = resp.json()

    assert resp.status_code == 200
    assert len(reservations) == 1
    assert reservations[0]['title'] == title
    assert reservations[0]['email'] == email
    assert 'timestamp' in reservations[0]
    assert 'reservation_id' in reservations[0]


def test_cancel_reservation():
    resp = requests.delete(f"{host}/request/1")

    assert resp.status_code == 204


def test_list_has_no_reservations_again():
    resp = requests.get(f"{host}/request")

    assert resp.status_code == 200
    assert resp.json() == []

