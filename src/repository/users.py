from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
        Retrieves a user by specific user email.

        :param email: User email.
        :type email: str
        :param db: The database session.
        :type db: Session
        :return: User.
        :rtype: User
        """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
        Creates a user by credentials included in UserModel

        :param body: UserModel.
        :type body: UserModel
        :param db: The database session.
        :type db: Session
        :return: New User.
        :rtype: User
        """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
        Updates a token of User

        :param user: Definite User.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: Token.
        :rtype: None
        """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
        Confirming of users email

        :param email: User's email.
        :type email: str
        :param db: The database session.
        :type db: Session
        :return: None.
        :rtype: None
        """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
        Updates user avatar

        :param email: User's email.
        :type email: str
        :param url: avatar url.
        :type url: str
        :param db: The database session.
        :type db: Session
        :return: User.
        :rtype: User
        """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user