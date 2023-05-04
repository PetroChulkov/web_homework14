import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from libgravatar import Gravatar
from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (get_user_by_email,
                                  create_user,
                                  update_avatar)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username="Example", email="example@exmpl.com")

    async def test_get_user_by_email(self):
        self.session.query(User).filter().first.return_value = self.user
        result = await get_user_by_email(email="example@exmpl.com", db=self.session)
        self.assertEqual(result, self.user)

    async def test_create_user(self):
        body = UserModel(username="Example", email="example@exmpl.com", password="qwerty")
        g = Gravatar(body.email)
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertEqual(result.avatar, g.get_image())
        self.assertTrue(hasattr(result, "id"))

    async def test_update_avatar(self):
        avatar_link = 'http://new_avatar'
        self.session.query(User).filter().first.return_value = self.user
        result = await update_avatar(email="example@exmpl.com", url=avatar_link, db=self.session)
        self.assertEqual(result.avatar, avatar_link)

if __name__ == '__main__':
    unittest.main()
