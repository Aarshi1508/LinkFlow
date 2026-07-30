"""
Tests for URL CRUD business logic - specifically the parts that matter
most in an interview: custom alias conflicts and ownership enforcement
(preventing one user from reading/editing/deleting another user's link).
"""


def test_create_short_url_with_custom_alias(client, auth_headers):
    response = client.post(
        "/shorten",
        json={"original_url": "https://example.com/docs", "custom_alias": "my-docs"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["short_code"] == "my-docs"
    assert body["original_url"] == "https://example.com/docs"
    assert body["total_clicks"] == 0


def test_create_url_with_duplicate_alias_is_rejected(client, auth_headers):
    client.post(
        "/shorten",
        json={"original_url": "https://example.com/one", "custom_alias": "taken"},
        headers=auth_headers,
    )

    response = client.post(
        "/shorten",
        json={"original_url": "https://example.com/two", "custom_alias": "taken"},
        headers=auth_headers,
    )

    assert response.status_code == 409


def test_owner_can_edit_their_own_url(client, auth_headers):
    created = client.post(
        "/shorten",
        json={"original_url": "https://example.com/old", "custom_alias": "editme"},
        headers=auth_headers,
    ).json()

    response = client.put(
        f"/urls/{created['id']}",
        json={"original_url": "https://example.com/new"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["original_url"] == "https://example.com/new"


def test_owner_can_delete_their_own_url(client, auth_headers):
    created = client.post(
        "/shorten",
        json={"original_url": "https://example.com/deleteme"},
        headers=auth_headers,
    ).json()

    delete_response = client.delete(f"/urls/{created['id']}", headers=auth_headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/urls/{created['id']}", headers=auth_headers)
    assert get_response.status_code == 404


def test_cannot_edit_another_users_url(client, auth_headers, other_user_auth_headers):
    # Created by user A.
    created = client.post(
        "/shorten",
        json={"original_url": "https://example.com/private"},
        headers=auth_headers,
    ).json()

    # User B tries to edit it.
    response = client.put(
        f"/urls/{created['id']}",
        json={"original_url": "https://example.com/hijacked"},
        headers=other_user_auth_headers,
    )

    assert response.status_code == 403


def test_cannot_delete_another_users_url(client, auth_headers, other_user_auth_headers):
    created = client.post(
        "/shorten",
        json={"original_url": "https://example.com/private"},
        headers=auth_headers,
    ).json()

    response = client.delete(f"/urls/{created['id']}", headers=other_user_auth_headers)

    assert response.status_code == 403
