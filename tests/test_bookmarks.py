import sys

import pytest
from sqlmodel import select

sys.path.append('.')
sys.path.append('..')

from app.bookmarks.crud import create_bookmark, get_or_create_tag
from app.bookmarks.models import BookmarkDb, TagDb
from app.database import get_test_db


def test_get_or_create_tag():
    for db in get_test_db():
        tag1 = get_or_create_tag(db, TagDb(name='video'))
        tag2 = get_or_create_tag(db, TagDb(name='video'))
        tag3 = get_or_create_tag(db, TagDb(name='hobby'))

        assert tag1 == tag2
        assert tag2 != tag3

        assert db.exec(select(TagDb)).all() == [tag1, tag3]


def test_create_bookmark_with_tags():
    for db in get_test_db():
        tags = [
            get_or_create_tag(db, TagDb(name='video')),
            get_or_create_tag(db, TagDb(name='hobby')),
        ]

        b = BookmarkDb(url='http://ya.ru', tags=tags)
        create_bookmark(db, b)
        assert b.tags == tags

        tags = [
            get_or_create_tag(db, TagDb(name='video')),
            get_or_create_tag(db, TagDb(name='mail')),
        ]

        b = BookmarkDb(url='http://mail.ru', tags=tags)
        create_bookmark(db, b)
        assert b.tags == tags


def test_get_bookmarks_by_tag():
    for db in get_test_db():
        tag1 = get_or_create_tag(db, TagDb(name='video'))
        tag2 = get_or_create_tag(db, TagDb(name='hobby'))
        tag3 = get_or_create_tag(db, TagDb(name='mail'))

        b1 = BookmarkDb(url='http://ya.ru', tags=[tag1, tag2])
        create_bookmark(db, b1)

        b2 = BookmarkDb(url='http://mail.ru', tags=[tag2, tag3])
        create_bookmark(db, b2)

        assert tag1.bookmarks == [b1]
        assert tag2.bookmarks == [b1, b2]
        assert tag3.bookmarks == [b2]
