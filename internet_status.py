import http.client


def is_connected():
    # Checks if internet connection is available
    conn = http.client.HTTPSConnection('8.8.8.8', timeout=5)
    try:
        conn.request('HEAD', '/')
        return True
    except Exception:
        return False
    finally:
        conn.close()
