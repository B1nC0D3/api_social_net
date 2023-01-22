from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_session


class BaseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _raise_exception(self, status, detail, headers=None):
        raise HTTPException(status_code=status,
                            detail=detail,
                            headers=headers)
