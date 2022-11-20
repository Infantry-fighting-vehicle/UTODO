from tabnanny import check
from sqlalchemy import true
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode
from schemas import *
from app import app

app.testing = True
client = app.test_client()

global test_user_id
test_user_id = 'not found'
test_user_json = {
    'name': 'John2',
    'surname': 'Jam2es2',
    'email': 'joh2n.james.2022@email.com',
    'password': 'qwerty22022'
}

def authentication_headers(email = test_user_json['email'], password = test_user_json['password']):
    return {'headers': {
            'Authorization': f'''Basic {b64encode(f"{email}:{password}".encode('UTF-8')).decode('UTF-8')}'''
        }
    }

def check_data(responce_json, compare_object):
    for x in compare_object.keys():
        if x == 'password':
            assert check_password_hash(responce_json[x], compare_object[x])
        else:
            assert responce_json[x] == compare_object[x]

##### USER

def test_create_user():
    global test_user_id

    res = client.post('/user', json=test_user_json)

    assert res.status_code == 200
    check_data(res.json, test_user_json)
    assert res.json.get('id')
    test_user_id = res.json['id']

def test_del_user_without_credentials():
    global test_user_id
    assert test_user_id != 'not found'
    res = client.delete(f'/user/{test_user_id}')
    assert res.status_code == 401

def test_login():
    global test_user_id

    res = client.get('/user/me', query_string = {
        'email': test_user_json['email'],
        'password': test_user_json['password']
    })

    assert res.status_code == 200
    check_data(res.json, test_user_json)
    assert res.json['id'] == test_user_id

def test_login_without_credentials():
    res = client.get('/user/me')
    assert res.status_code == 404

def test_login_without_password():
    res = client.get('/user/me', query_string = {'email': test_user_json['email']})
    assert res.status_code == 403

def test_get_tasks():
    res = client.get(f'/user/tasks', **authentication_headers())

    assert res.status_code == 200
    assert res.json == []

##### GROUP
global test_group_id
test_group_id = 'not found'
test_group_json = {
  'name': 'KN-217 Tasks',
  'description': 'This group is created to check KN-217 progress'
}

def test_group_create():
    global test_group_id, test_user_id

    res = client.post('/groups', json=test_group_json, **authentication_headers())

    assert res.status_code == 200
    check_data(res.json, test_group_json)
    assert res.json.get('id')
    test_group_id = res.json['id']
    assert res.json.get('owner_id') == test_user_id

def test_get_groups():
    global test_group_id
    res = client.get('/groups', **authentication_headers())

    assert res.status_code == 200
    for group in res.json:
        if group['id'] == test_group_id:
            return
    assert False ## group not found

def test_get_not_existing_group_by_id():
    global test_group_id
    res = client.get(f'/groups/0', **authentication_headers())

    assert res.status_code == 404
    
def test_get_group_by_invalid_id():
    global test_group_id
    res = client.get(f'/groups/-1', **authentication_headers())

    assert res.status_code == 400

def test_get_group_by_id():
    global test_group_id
    res = client.get(f'/groups/{test_group_id}', **authentication_headers())

    assert res.status_code == 200
    check_data(res.json, test_group_json)
    assert res.json.get('owner_id') == test_user_id

def test_edit_group():
    global test_group_id
    test_group_json['name'] = 'KN-216 Tasks'
    res = client.put(f'/groups/{test_group_id}', query_string=test_group_json, **authentication_headers())

    assert res.status_code == 200
    check_data(res.json, test_group_json)

def test_group_members():
    global test_group_id
    res = client.get(f'/groups/{test_group_id}/members', **authentication_headers())

    assert res.status_code == 200
    assert len(res.json) == 1
    public_test_user = test_user_json.copy()
    del public_test_user['password']
    check_data(res.json[0], public_test_user)

global test_new_member

def test_group_invite_member():
    global test_new_member, test_group_id
    test_member_json = {
        'name': 'Bill2',
        'surname': 'Robinson2',
        'email': 'bill.robinson.2022@email.com',
        'password': 'qwerty22022'
    }
    res = client.post('/user', json=test_member_json)

    assert res.status_code == 200
    check_data(res.json, test_member_json)
    assert res.json.get('id')
    test_new_member = res.json['id']

    res = client.post(f'/groups/{test_group_id}/members', query_string={'email': test_member_json['email']}, **authentication_headers())
    assert res.status_code == 200
    del test_member_json['password']
    check_data(res.json, test_member_json)
    assert res.json['group_id'] == test_group_id
    assert res.json['user_id'] == test_new_member

    res = client.get(f'/groups/{test_group_id}/members', **authentication_headers())

    assert res.status_code == 200
    assert len(res.json) == 2
    check_data(res.json[1], test_member_json)

def test_group_delete_member():
    global test_new_member, test_group_id
    res = client.delete(f'/groups/{test_group_id}/members', query_string={'member_id': test_new_member}, **authentication_headers())
    assert res.status_code == 200

    res = client.delete(f'/user/{test_new_member}', **authentication_headers('bill.robinson.2022@email.com', 'qwerty22022'))
    assert res.status_code == 200

global test_task_id
test_task_json = {
  'name': 'lab 3 PP',
  'description': 'deadline by 29.09.2022 (after it half a number of points)'
}

def test_group_add_tasks():
    global test_group_id
    res = client.post(f'/groups/{test_group_id}/tasks', json = test_task_json, **authentication_headers())

    assert res.status_code == 200

def test_group_tasks_list():
    global test_group_id, test_task_id
    res = client.get(f'/groups/{test_group_id}/tasks', **authentication_headers())

    assert res.status_code == 200
    assert len(res.json) == 1
    assert test_group_id == res.json[0]['group_id']
    check_data(res.json[0], test_task_json)
    assert res.json[0].get('id')
    test_task_id = res.json[0]['id']

def test_invalid_group_tasks_list():
    res = client.get(f'/groups/0/tasks', **authentication_headers())

    assert res.status_code == 404

def test_get_task_by_id():
    global test_task_id, test_group_id
    res = client.get(f'/groups/{test_group_id}/tasks/{test_task_id}', **authentication_headers())

    assert res.status_code == 200
    assert test_group_id == res.json['group_id']
    assert test_task_id == res.json['id']
    check_data(res.json, test_task_json)

def test_get_user_task():
    res = client.get(f'/user/tasks', **authentication_headers())

    assert res.status_code == 200
    assert len(res.json) == 1

def test_get_user_task_by_id():
    global test_task_id, test_group_id
    res = client.get(f'/user/tasks/{test_task_id}', **authentication_headers())

    assert res.status_code == 200
    check_data(res.json, test_task_json)

def test_update_user_task_done():
    global test_task_id
    res = client.put(f'/user/tasks/{test_task_id}', query_string={'status': 'done'}, **authentication_headers())

    assert res.status_code == 200
    assert res.json['status'] == 'done'

def test_update_user_task_undone():
    global test_task_id
    res = client.put(f'/user/tasks/{test_task_id}', query_string={'status': 'undone'}, **authentication_headers())

    assert res.status_code == 200
    assert res.json['status'] == 'undone'

def test_del_task():
    global test_task_id, test_group_id
    res = client.delete(f'/groups/{test_group_id}/tasks/{test_task_id}', **authentication_headers())

    assert res.status_code == 200

def test_get_deleted_task_by_id():
    global test_task_id, test_group_id
    res = client.get(f'/groups/{test_group_id}/tasks/{test_task_id}', **authentication_headers())

    assert res.status_code == 404

def test_del_group():
    global test_group_id
    res = client.delete(f'/groups/{test_group_id}', **authentication_headers())

    assert res.status_code == 200
    try:
        test_get_group_by_id()
    except AssertionError:
        return
    assert False # group has not be found

def test_del_user():
    global test_user_id
    assert test_user_id != 'not found'
    res = client.delete(f'/user/{test_user_id}', **authentication_headers())
    assert res.status_code == 200