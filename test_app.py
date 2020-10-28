import app as web

app = web.app.test_client()

def test_main():
    rv = app.get('/')
    assert rv.status == '200 OK'
    assert b'<h1>Welcome to Flask Login Example</h1>' in rv.data


def test_protected():
    rv = app.get('/protected')
    assert rv.status == '401 UNAUTHORIZED'
    print(rv.data)
    assert b'<h1>Unauthorized</h1>' in rv.data
