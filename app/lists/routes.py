from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_db
from app.lists.crud import get_list_by_id, get_or_create_list, get_user_lists
from app.lists.models import BookmarkList

router = APIRouter()


@router.get('/users/{user_id}/lists', response_model=List[BookmarkList])
def get_lists_of_user_endopint(
    user_id: int,
    *,
    db: Session = Depends(get_db),
    bookmarklist: BookmarkList,
):
    return get_user_lists(db, user_id)


@router.post('/lists')
def create_bookmarklist_endpoint(
    *,
    db: Session = Depends(get_db),
    bookmarklist: BookmarkList,
):
    get_or_create_list(db, bookmarklist)


@router.get('/lists/{list_id}', response_model=Optional[BookmarkList])
def get_bookmarklist_by_id_endpoint(
    list_id: int,
    *,
    db: Session = Depends(get_db),
):
    return get_list_by_id(db, list_id)
