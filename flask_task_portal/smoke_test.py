from run import app

client = app.test_client()
response = client.get('/')
assert response.status_code == 200
assert b'Simple Library Management' in response.data
print('Application factory and home route smoke test passed.')
