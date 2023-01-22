import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError

from api.models.auth import Token, User, UserCreate
from database import tables
from services.base import BaseService
from settings import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService(BaseService):

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        return bcrypt.hash(plain_password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={
                    'WWW-Authenticate': 'Bearer'
                }
        )

        try:
            payload = jwt.decode(
                    token,
                    settings.jwt_secret,
                    algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)

        now = datetime.datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(days=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
                payload,
                settings.jwt_secret,
                algorithm=settings.jwt_algorithm,
        )

        return Token(access_token=token)

    def register_new_user(self, user_data: UserCreate, ) -> Token:
        user = tables.User(
                email=user_data.email,
                username=user_data.username,
                password_hash=self.hash_password(user_data.password),
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception_data = {
            'status_code': status.HTTP_401_UNAUTHORIZED,
            'detail': 'Could not validate credentials',
            'headers': {
                'WWW-Authenticate': 'Bearer'}
        }

        user = (self.session
                .query(tables.User)
                .filter(tables.User.username == username)
                .first()
                )
        if not user:
            self._raise_exception(**exception_data)

        if not self.verify_password(password, user.password_hash):
            self._raise_exception(**exception_data)

        return self.create_token(user)
