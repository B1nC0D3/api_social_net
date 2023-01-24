from fastapi import status

from database.tables import Dislikes, Likes, Post
from services.base import BaseService


class BaseScore(BaseService):

    def get_scores(self, post_id: int):
        return self._get_scores(post_id)

    def _return_author_if_post_exists(self, post_id: int) -> int:
        post = (self.session
                .query(Post)
                .filter(Post.id == post_id)
                .first())
        if not post:
            self._raise_exception(
                    status=status.HTTP_404_NOT_FOUND,
                    detail='Post not found')
        return post.author_id

    def _is_author(self, user_id: int, author_id: int):
        if author_id == user_id:
            self._raise_exception(
                    status=status.HTTP_400_BAD_REQUEST,
                    detail='You cant score your own posts')

    def _find_like_if_exists(self, user_id: int, post_id: int) -> Likes | None:
        like = (self.session
                .query(Likes)
                .filter(Likes.post_id == post_id)
                .filter(Likes.user_id == user_id)
                .first())
        return like

    def _find_dislike_if_exists(self, user_id: int, post_id: int) -> Dislikes | None:
        dislike = (self.session
                   .query(Dislikes)
                   .filter(Dislikes.post_id == post_id)
                   .filter(Dislikes.user_id == user_id)
                   .first())
        return dislike

    def _get_scores(self, post_id: int):
        scores = (self.session
                  .query(Post.likes, Post.dislikes)
                  .filter(Post.id == post_id)
                  .first())
        if not scores:
            self._raise_exception(
                    status=status.HTTP_404_NOT_FOUND,
                    detail='Post not found'
            )
        return scores


class LikesService(BaseScore):

    def create(self, user_id: int, post_id: int):
        author_id = self._return_author_if_post_exists(post_id)
        self._is_author(user_id, author_id)
        if self._find_like_if_exists(user_id, post_id):
            self._raise_exception(
                    status=status.HTTP_400_BAD_REQUEST,
                    detail='You already liked this post')
        dislike = self._find_dislike_if_exists(user_id, post_id)
        if dislike:
            self.session.delete(dislike)
        like = Likes(
                user_id=user_id,
                post_id=post_id
        )
        self.session.add(like)
        self.session.commit()
        return self._get_scores(post_id)

    def delete(self, user_id: int, post_id: int):
        author_id = self._return_author_if_post_exists(post_id)
        self._is_author(user_id, author_id)
        if not self._find_like_if_exists(user_id, post_id):
            self._raise_exception(
                    status=status.HTTP_400_BAD_REQUEST,
                    detail='You dont liked this post yet')

        like = (self.session
                .query(Likes)
                .filter(Likes.user_id == user_id)
                .filter(Likes.post_id == post_id)
                .first())
        self.session.delete(like)
        self.session.commit()
        return self._get_scores(post_id)


class DislikesService(BaseScore):

    def create(self, user_id: int, post_id: int):
        author_id = self._return_author_if_post_exists(post_id)
        self._is_author(user_id, author_id)
        if self._find_dislike_if_exists(user_id, post_id):
            self._raise_exception(
                    status=status.HTTP_400_BAD_REQUEST,
                    detail='You already disliked this post')

        like = self._find_like_if_exists(user_id, post_id)
        if like:
            self.session.delete(like)
        dislike = Dislikes(
                user_id=user_id,
                post_id=post_id
        )
        self.session.add(dislike)
        self.session.commit()
        return self._get_scores(post_id)

    def delete(self, user_id: int, post_id: int):
        author_id = self._return_author_if_post_exists(post_id)
        self._is_author(user_id, author_id)
        if not self._find_dislike_if_exists(user_id, post_id):
            self._raise_exception(
                    status=status.HTTP_400_BAD_REQUEST,
                    detail='You dont disliked this post yet')

        dislike = (self.session
                   .query(Dislikes)
                   .filter(Dislikes.user_id == user_id)
                   .filter(Dislikes.post_id == post_id)
                   .first())
        self.session.delete(dislike)
        self.session.commit()
        return self._get_scores(post_id)
