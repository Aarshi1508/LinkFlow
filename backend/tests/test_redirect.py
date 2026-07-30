"""
Tests for the public redirect endpoint - the one route with no auth
requirement, and the one responsible for click analytics.
"""


def test_valid_short_code_redirects_to_original_url(client, auth_headers):
    created = client.post(
        "/shorten",
        json={"original_url": "https://example.com/target", "custom_alias": "goto"},
        headers=auth_headers,
    ).json()

    # follow_redirects=False: we want to inspect the redirect response
    # itself (status + Location header), not actually follow it out to
    # example.com.
    response = client.get(f"/link/{created['short_code']}", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/target"


def test_unknown_short_code_returns_404(client):
    response = client.get("/link/does-not-exist", follow_redirects=False)

    assert response.status_code == 404


def test_click_counter_increments_on_each_redirect(client, auth_headers):
    created = client.post(
        "/shorten",
        json={"original_url": "https://example.com/popular", "custom_alias": "hot-link"},
        headers=auth_headers,
    ).json()

    client.get("/link/hot-link", follow_redirects=False)
    client.get("/link/hot-link", follow_redirects=False)
    client.get("/link/hot-link", follow_redirects=False)

    details = client.get(f"/urls/{created['id']}", headers=auth_headers).json()

    assert details["total_clicks"] == 3
    assert details["last_visited"] is not None
