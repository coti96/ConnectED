import json
import urllib.request
import urllib.error


def http_json(method: str, url: str, payload=None, headers=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url=url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return e.code, body


def main():
    base = "http://localhost:5000"

    login_status, login_body = http_json(
        "POST",
        f"{base}/login",
        payload={"email": "paul@etudiant.com", "password": "password"},
    )
    print("LOGIN", login_status)
    print(login_body)

    if login_status != 200:
        return

    token = json.loads(login_body).get("token")
    print("TOKEN_LEN", len(token) if token else None)

    dash_status, dash_body = http_json(
        "GET",
        f"{base}/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )
    print("DASHBOARD", dash_status)
    print(dash_body)

    rec_status, rec_body = http_json(
        "GET",
        f"{base}/projects/recommended",
        headers={"Authorization": f"Bearer {token}"},
    )
    print("RECOMMENDED", rec_status)
    print(rec_body[:500])


if __name__ == "__main__":
    main()

