from fastapi import APIRouter, Depends, status

from api.models.auth import User
from api.models.post import PostCreate, PostResponse
from services.auth import get_current_user
from services.posts import PostService

router = APIRouter(
        prefix='/posts'
)


@router.get('/', response_model=list[PostResponse])
def get_posts(post_service: PostService = Depends(),
              user: User = Depends(get_current_user)):
    return post_service.get_many(user.id)


@router.get('/{post_id}', response_model=PostResponse)
def get_post(post_id: int,
             user: User = Depends(get_current_user),
             post_service: PostService = Depends()):
    return post_service.get(user.id, post_id)


@router.post('/', response_model=PostResponse,
             status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate,
                user: User = Depends(get_current_user),
                post_service: PostService = Depends()):
    return post_service.create(user.id, post_data)


@router.patch('/{post_id}', response_model=PostResponse)
def update_post(post_id: int, post_data: PostCreate,
                user: User = Depends(get_current_user),
                post_service: PostService = Depends()):
    return post_service.update(user.id, post_id, post_data)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
                user: User = Depends(get_current_user),
                post_service: PostService = Depends()):
    return post_service.delete(user.id, post_id)
