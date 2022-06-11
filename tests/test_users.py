import sys

import pytest
import uuid

sys.path.append('.')

from app.database import User, get_test_db, get_user_by_token, get_user_by_username, update_user_token

# TODO:
# - [x] Test get user by token
# - [x] Test update token
# - [x] Test that token is unique

def test_create_user():
    for db in get_test_db():
        assert (get_user_by_username(db, 'Alex') is None)

        test_user = User(username='Alex', password_hash='123')
        db.add(test_user)
        db.commit()

        assert (get_user_by_username(db, 'Alex') == test_user)


def test_unique_username():
    for db in get_test_db():
        test_user = User(username='Alex', password_hash='123')
        db.add(test_user)
        db.commit()

        test_user = User(username='Alex', password_hash='1234')
        db.add(test_user)

        with pytest.raises(Exception):
            db.commit()


def test_update_token():
    for db in get_test_db():
        test_user = User(username='Alex', password_hash='123')
        db.add(test_user)
        db.commit()

        access_token = str(uuid.uuid4())
        update_user_token(db, test_user, access_token)

        assert (get_user_by_username(db, 'Alex').token == access_token)


def test_get_user_by_token():
    for db in get_test_db():
        access_token = str(uuid.uuid4())
        expected_user = User(username='Alex', password_hash='123', token=access_token)
        db.add(expected_user)
        db.commit()

        expected_user =  get_user_by_username(db, 'Alex')
        assert (get_user_by_token(db, expected_user.token) == expected_user)


def test_unique_token():
    for db in get_test_db():
        access_token = str(uuid.uuid4())
        test_user = User(username='Alex', password_hash='123', token=access_token)
        db.add(test_user)
        db.commit()

        test_user = User(username='Alexs', password_hash='1234', token=access_token)
        db.add(test_user)

        with pytest.raises(Exception):
            db.commit()
