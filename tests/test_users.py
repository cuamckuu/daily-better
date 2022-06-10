import sys

import pytest

sys.path.append('.')

from app.database import User, get_db, get_user_by_username


def test_create_user():
    for db in get_db(is_test=True):
        assert (get_user_by_username(db, 'Alex') is None)

        test_user = User(username='Alex', password_hash='123')
        db.add(test_user)
        db.commit()

        assert (get_user_by_username(db, 'Alex') == test_user)


def test_unique_username():
    for db in get_db(is_test=True):
        test_user = User(username='Alex', password_hash='123')
        db.add(test_user)

        db.commit()

        test_user = User(username='Alex', password_hash='1234')
        db.add(test_user)

        with pytest.raises(Exception):
            db.commit()
