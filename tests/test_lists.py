import sys

import pytest

sys.path.append('.')
sys.path.append('..')

from app.database import get_test_db
from app.lists.crud import (create_list, delete_list_by_id, get_list_by_id,
                            get_user_lists, update_list_by_id)
from app.lists.models import BookmarkList
from app.users.models import User


def test_create_list():
    for db in get_test_db():
        assert (get_list_by_id(db, 1) is None)
        
        test_list = BookmarkList(name='List1')
        create_list(db, test_list)

        assert (get_list_by_id(db, 1) == test_list)


def test_update_list():
    for db in get_test_db():
        test_list = BookmarkList(name='List1')
        db.add(test_list)
        db.commit()

        assert (get_list_by_id(db, 1).name == 'List1')
        update_list_by_id(db, 1, 'NewName')
        
        assert (get_list_by_id(db, 1).name == 'NewName')


def test_delete_list():
    for db in get_test_db():
        test_list = BookmarkList(name='List1')
        db.add(test_list)
        db.commit()

        assert (get_list_by_id(db, 1) != None)

        delete_list_by_id(db, 1)

        assert (get_list_by_id(db, 1) == None)


def test_get_users_lists():
    for db in get_test_db():
        test_user = User(username='Alex', password_hash='123')
        test_list = BookmarkList(name='List1', user=test_user)
        test_list2 = BookmarkList(name='List2', user=test_user)
        db.add(test_user)
        db.commit()

        assert (get_user_lists(db, test_user.id)[0] == test_list)
        assert (get_user_lists(db, test_user.id)[1] == test_list2)