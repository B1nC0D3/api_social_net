from fastapi import APIRouter, Depends, status

from api.models.scores import ScoresResponse
from api.models.auth import User
from services.auth import get_current_user
from services.scores import DislikesService, LikesService, BaseScore
from redis import Redis
from redis.commands.json.path import Path


router = APIRouter(
        prefix='/posts/{post_id}'
)
redis = None


@router.on_event('startup')
def on_startup():
    global redis
    redis = Redis('redis', 6379)


@router.on_event('shutdown')
def on_shutdown():
    redis.close()


@router.get('/scores', response_model=ScoresResponse)
def get_scores(post_id: int,
               user: User = Depends(get_current_user),
               service: BaseScore = Depends()):
    cached_scores = redis.get(post_id)
    if cached_scores:
        likes, dislikes = cached_scores.split()
        return {'likes': likes,
                'dislikes': dislikes
                }
    scores = service.get_scores(post_id)
    scores_to_cache = ScoresResponse.parse_obj(scores).dict()
    redis.set(post_id, f'{scores_to_cache.get("likes")} {scores_to_cache.get("dislikes")}')
    return scores


@router.post('/like', status_code=status.HTTP_201_CREATED,
             response_model=ScoresResponse)
def create_like(post_id: int,
                user: User = Depends(get_current_user),
                like_service: LikesService = Depends()):
    scores = like_service.create(user.id, post_id)
    scores_to_cache = ScoresResponse.parse_obj(scores).dict()
    redis.set(post_id, f'{scores_to_cache.get("likes")} {scores_to_cache.get("dislikes")}')
    return scores



@router.delete('/like', status_code=status.HTTP_200_OK,
               response_model=ScoresResponse)
def delete_like(post_id: int,
                user: User = Depends(get_current_user),
                like_service: LikesService = Depends()):
    scores = like_service.delete(user.id, post_id)
    scores_to_cache = ScoresResponse.parse_obj(scores).dict()
    redis.set(post_id, f'{scores_to_cache.get("likes")} {scores_to_cache.get("dislikes")}')
    return scores


@router.post('/dislike', status_code=status.HTTP_201_CREATED,
             response_model=ScoresResponse)
def create_dislike(post_id: int,
                   user: User = Depends(get_current_user),
                   dislike_service: DislikesService = Depends()):
    scores = dislike_service.create(user.id, post_id)
    scores_to_cache = ScoresResponse.parse_obj(scores).dict()
    redis.set(post_id, f'{scores_to_cache.get("likes")} {scores_to_cache.get("dislikes")}')
    return scores


@router.delete('/dislike', status_code=status.HTTP_200_OK,
               response_model=ScoresResponse)
def delete_dislike(post_id: int,
                   user: User = Depends(get_current_user),
                   dislike_service: DislikesService = Depends()):
    scores = dislike_service.delete(user.id, post_id)
    scores_to_cache = ScoresResponse.parse_obj(scores).dict()
    redis.set(post_id, f'{scores_to_cache.get("likes")} {scores_to_cache.get("dislikes")}')
    return scores
