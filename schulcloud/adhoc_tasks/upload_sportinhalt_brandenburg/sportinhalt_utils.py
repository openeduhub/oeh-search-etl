def get_base_headers(auth_response):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": auth_response.headers.get("Set-Cookie"),
    }
    return headers