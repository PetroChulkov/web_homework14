import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate, ContactResponse
from src.repository.contacts import (
    show_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    search_contacts,
    upcoming_birthday,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_show_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await show_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactBase(name="test", surname="test surname", email="testemail@email.com", phone="+421123456789", born_date="2023-04-26T09:31:02.618Z")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.born_date, body.born_date)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactUpdate(name="test", surname="test surname", email="testemail@email.com", phone="+421123456789", born_date="2023-04-26T09:31:02.618Z", done="True")
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactUpdate(name="test", surname="test surname", email="testemail@email.com", phone="+421123456789", born_date="2023-04-26T09:31:02.618Z", done="True")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts_found(self):
        result = await search_contacts(credentials="test", user=self.user, db=self.session)
        print(result)
        self.assertTrue(result)

    async def test_search_contacts_not_found(self):
        body = ContactBase(name="test", surname="test surname", email="testemail@email.com", phone="+421123456789", born_date="2023-04-26T09:31:02.618Z")
        result = await search_contacts(credentials="test", user=self.user, db=self.session)
        self.assertNotEqual(result.name, body.name)

    async def test_upcoming_birthday(self):

        body = ContactBase(name="test", surname="test surname", email="testemail@email.com", phone="+421123456789",
                           born_date="2023-04-27T09:31:02.618Z")
        await create_contact(body=body, user=self.user, db=self.session)
        result = await upcoming_birthday(user=self.user, db=self.session)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
