import app as web

app = web.app.test_client()

def test_main():
    rv = app.get('/')
    assert rv.status == '200 OK'
    assert b'<h1>Welcome to Flask Login Example</h1>' in rv.data


def test_protected():
    rv = app.get('/protected')
    assert rv.status == '401 UNAUTHORIZED'
    #print(rv.data)
    assert b'<h1>Unauthorized</h1>' in rv.data

# TODO maybe logout should return an error if we are not logged in
def test_logout():
    rv = app.get('/logout')
    assert rv.status == '200 OK'
    #print(rv.data)
    assert b'<title>Logged out</title>' in rv.data


def test_login_process():
    rv = app.get('/protected')
    assert rv.status == '401 UNAUTHORIZED'
    assert b'<h1>Unauthorized</h1>' in rv.data

    rv = app.get('/login')
    assert rv.status == '200 OK'
    assert b'<title>Login</title>' in rv.data
    #print(rv.data)

    rv = app.post('/login', data = {
        'email': 'foo@bar.tld',
        'password': 'secret'
    })
    assert rv.status == '302 FOUND'
    #print(rv.data)
    #print(rv.headers)
    assert rv.headers['Location'] == 'http://localhost/protected'
    assert b'<title>Redirecting...</title>' in rv.data

    rv = app.get('/protected')
    assert rv.status == '200 OK'
    #print(rv.data)
    assert b'<title>Protected</title>' in rv.data

    rv = app.get('/logout')
    assert rv.status == '200 OK'
    #print(rv.data)
    assert b'<title>Logged out</title>' in rv.data

    rv = app.get('/protected')
    assert rv.status == '401 UNAUTHORIZED'
    assert b'<h1>Unauthorized</h1>' in rv.data


def test_failed_login_process():
    rv = app.get('/protected')
    assert rv.status == '401 UNAUTHORIZED'
    assert b'<h1>Unauthorized</h1>' in rv.data

    rv = app.post('/login', data = {
        'email': 'foo@bar.tld',
        'password': 'wrong password'
    })
    assert rv.status == '401 UNAUTHORIZED'
    #print(rv.data)
    assert b'<title>Bad Login</title>' in rv.data
    