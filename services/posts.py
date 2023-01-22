from fastapi import HTTPException, status

from api.models.post import PostCreate
from database.tables import Post
from services.base import BaseService


class PostService(BaseService):

    def get_many(self, user_id: int) -> list[Post]:
        posts = (self.session
                 .query(Post)
                 .all()
                 )
        for post in posts:
            post.is_author = user_id == post.author_id
        return posts

    def get(self, user_id: int, post_id: int) -> Post:
        return self._get(user_id, post_id)

    def create(self, user_id: int, post_data: PostCreate) -> Post:
        post = Post(
                author_id=user_id,
                text=post_data.text
        )
        self.session.add(post)
        self.session.commit()
        post.is_author = user_id == post.author_id
        return post

    def update(self, user_id: int, post_id: int, post_data: PostCreate) -> Post:
        post = self._get(user_id, post_id)
        self._is_author(user_id, post.author_id)
        for key, value in post_data:
            setattr(post, key, value)
        self.session.commit()
        return post

    def delete(self, user_id: int, post_id: int):
        post = self._get(user_id, post_id)
        self._is_author(user_id, post.author_id)
        self.session.delete(post)
        self.session.commit()

    def _get(self, user_id: int, post_id: int) -> Post:
        post = (self.session
                .query(Post)
                .filter(Post.id == post_id)
                .first())
        if not post:
            self._raise_exception(status=status.HTTP_404_NOT_FOUND,
                                  detail='Post not found')
        post.is_author = user_id == post.author_id
        return post

    def _is_author(self, user_id: int, author_id: int):
        if user_id != author_id:
            self._raise_exception(
                    status=status.HTTP_400_BAD_REQUEST,
                    detail='You are not the author')
