from fastapi import APIRouter, Depends, status

from api.models.auth import User
from services.auth import get_current_user
from services.scores import DislikesService, LikesService

router = APIRouter(
        prefix='/posts/{post_id}'
)


@router.post('/like', status_code=status.HTTP_201_CREATED)
def create_like(post_id: int,
                user: User = Depends(get_current_user),
                like_service: LikesService = Depends()):
    like_service.create(user.id, post_id)


@router.delete('/like', status_code=status.HTTP_204_NO_CONTENT)
def delete_like(post_id: int,
                user: User = Depends(get_current_user),
                like_service: LikesService = Depends()):
    like_service.delete(user.id, post_id)


@router.post('/dislike', status_code=status.HTTP_201_CREATED)
def create_dislike(post_id: int,
                   user: User = Depends(get_current_user),
                   dislike_service: DislikesService = Depends()):
    dislike_service.create(user.id, post_id)


@router.delete('/dislike', status_code=status.HTTP_204_NO_CONTENT)
def delete_dislike(post_id: int,
                   user: User = Depends(get_current_user),
                   dislike_service: DislikesService = Depends()):
    dislike_service.delete(user.id, post_id)
