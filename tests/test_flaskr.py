def test_get_todos(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'{}\n' in response.data

def test_post_todo(test_client):
    response = test_client.post('/', data=dict(task='buy cats'))
    assert response.status_code == 201
    # Ask about the setup of this and the string placements
    assert b'"Added to todos: buy cats"\n' in response.data




