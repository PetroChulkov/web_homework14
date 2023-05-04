from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactResponse, ContactUpdate


async def show_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
        Retrieves a list of contacts for a specific user with specified pagination parameters.

        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param user: The user to retrieve contacts for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: A list of contacts.
        :rtype: List[Contact]
        """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
        Retrieves a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to retrieve.
        :type contact_id: int
        :param user: The user to retrieve the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The contact with the specified ID, or None if it does not exist.
        :rtype: Note | None
        """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    """
        Creates a new contact for a specific user.

        :param body: The data for the contact to create.
        :type body: ContactModel
        :param user: The user to create the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The newly created contact.
        :rtype: Contact
        """
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, born_date=body.born_date, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
        Removes a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to remove.
        :type contact_id: int
        :param user: The user to remove the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The removed contact, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
        Updates a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to update.
        :type contact_id: int
        :param body: The updated data for the contact.
        :type body: ContactUpdate
        :param user: The user to update the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The updated contact, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.born_date = body.born_date
        db.commit()
    return contact

async def search_contacts(credentials: str, user: User, db: Session) -> Contact:
    """
        Searches a single contact with the specified credentials for a specific user.

        :param credentials: Credentilas of the contact to search.
        :type credentials: int
        :param user: The user to search the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The searched contact, or None if it does not exist.
        :rtype: Contact | None
        """
    request = "%{}%".format(credentials)
    if db.query(Contact).filter(Contact.name.like(request), Contact.user_id == user.id).all():
        result = db.query(Contact).filter(Contact.name.like(request), Contact.user_id == user.id).all()
        return result
    if db.query(Contact).filter(Contact.surname.like(request), Contact.user_id == user.id).all():
        result = db.query(Contact).filter(Contact.surname.like(request), Contact.user_id == user.id).all()
        return result
    if db.query(Contact).filter(Contact.email.like(request), Contact.user_id == user.id).all():
        result = db.query(Contact).filter(Contact.email.like(request), Contact.user_id == user.id).all()
        return result

async def upcoming_birthday(user: User, db: Session):
    """
        Searches contacts with the upcoming birthdays in the future 7 days from current date.

        :param user: The user to search the birthdays for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The list of contacts, or None if it does not exist.
        :rtype: result | None
        """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    result = []
    today = datetime.now()

    for contact in contacts:
        day = today.day
        month = today.month
        year = contact.born_date.year
        try:
            first_day = datetime(year=year, month=month, day=day)
        except:
            first_day = datetime(year=year, month=3, day=1)
        last_day = today + timedelta(days=7)
        if first_day <= contact.born_date <= last_day:
            result.append(contact)

    return result

