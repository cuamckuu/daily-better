import sys

import pytest
from sqlmodel import select

sys.path.append('.')
sys.path.append('..')

from app.database import get_test_db
from app.lists.crud import (delete_list_by_id, get_list_by_id,
                            get_or_create_list, get_user_lists,
                            update_list_by_id)
from app.lists.models import BookmarkList
from app.users.models import User
from app.bookmarks.models import BookmarkDb, TagDb
from app.bookmarks.crud import create_bookmark, get_or_create_tag


def test_create_list():
    for db in get_test_db():
        all_lists = db.exec(select(BookmarkList)).all()

        assert len(all_lists) == 0

        test_list = BookmarkList(name='List1')
        new_list = get_or_create_list(db, test_list)

        assert (get_list_by_id(db, new_list.id) == test_list)


def test_update_list():
    for db in get_test_db():
        test_list = BookmarkList(name='List1')
        new_list = get_or_create_list(db, test_list)

        assert (get_list_by_id(db, new_list.id) == test_list)

        new_name = 'NewName'
        update_list_by_id(db, new_list.id, new_name)

        assert (get_list_by_id(db, new_list.id).name == new_name)


def test_delete_list():
    for db in get_test_db():
        test_list = BookmarkList(name='List1')
        new_list = get_or_create_list(db, test_list)

        delete_list_by_id(db, new_list.id)

        assert (get_list_by_id(db, new_list.id) is None)


def test_get_users_lists():
    for db in get_test_db():
        test_user = User(username='Alex', password_hash='123')
        test_list = BookmarkList(name='List1', user=test_user)
        test_list2 = BookmarkList(name='List2', user=test_user)
        db.add(test_user)
        db.commit()

        assert (get_user_lists(db, test_user.id) == [test_list, test_list2])


def test_unique_bookmarkslist():
    for db in get_test_db():
        test_user = User(username='Alex', password_hash='123')
        test_user2 = User(username='Step', password_hash='123')
        test_list = BookmarkList(name='List1', user=test_user)
        test_list2 = BookmarkList(name='List1', user=test_user2)
        db.add(test_user)
        db.add(test_user2)
        db.commit()

        assert (get_user_lists(db, test_user.id)[0] == test_list)
        assert (get_user_lists(db, test_user2.id)[0] == test_list2)

        test_list3 = BookmarkList(name='List1', user=test_user2)
        db.add(test_list3)
        with pytest.raises(Exception):
            db.commit()


def test_get_bookmarks_from_list():
    for db in get_test_db():
        tag1 = get_or_create_tag(db, TagDb(name='video'))
        tag2 = get_or_create_tag(db, TagDb(name='hobby'))
        tag3 = get_or_create_tag(db, TagDb(name='mail'))

        b1 = BookmarkDb(url='http://ya.ru', tags=[tag1, tag2])
        create_bookmark(db, b1)

        b2 = BookmarkDb(url='http://mail.ru', tags=[tag2, tag3])
        create_bookmark(db, b2)

        test_list = BookmarkList(name='List1', bookmarks=[b1, b2])

        db.add(test_list)
        db.commit()
        db.refresh(test_list)

        test_list = get_list_by_id(db, test_list.id)

        assert (test_list.bookmarks == [b1, b2])
