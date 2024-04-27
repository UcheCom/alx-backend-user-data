#!/usr/bin/env python3
"""
Main file
"""
import requests
from collections.abc import Mapping

LOC_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """This tests registered user"""
    resp = requests.post(f"{LOC_URL}/users",
                         data={"email": email, "password": password})
    assert resp.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """This tests the /sessions route with wrong password
    """
    resp = requests.post(f"{LOC_URL}/sessions",
                         data={"email": email, "password": password})
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """This tests the /sessions route with the correct credentials
    """
    resp = requests.post(f"{LOC_URL}/sessions",
                         data={"email": email, "password": password})
    assert resp.status_code == 200
    return resp.cookies.get("session_id")


def profile_unlogged() -> None:
    """ This tests the /profile route for a non login user
    """
    resp = requests.get(f"{LOC_URL}/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """This tests the /profile route for a logged in user"""
    resp = requests.get(f"{LOC_URL}/profile",
                        cookies={"session_id": session_id})
    assert resp.status_code == 200


def log_out(session_id: str) -> None:
    """This tests the /profile route for a logged out user"""
    resp = requests.get(f"{LOC_URL}/sessions",
                        cookies={"session_id": session_id})
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """This tests the /reset_password route"""
    resp = requests.get(f"{LOC_URL}/reset_password",
                        data={"email": email})
    assert resp.status_code == 200
    return resp.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """This tests the /reset_password route to update a user password"""
    resp = requests.put(f"{LOC_URL}/reset_password",
                        data={"email": email,
                              "reset_token": reset_token,
                              "new_password": new_password})
    assert resp.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
