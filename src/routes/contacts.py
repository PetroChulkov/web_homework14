from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.database.models import User
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def show_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
        The route is intended for receiving a list of contacts

        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param current_user: The user to retrieve contacts for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: A list of contacts.
        :rtype: List[Contact]
        """
    contacts = await repository_contacts.show_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
        The route is intended for receiving a contact by id

        :param contact_id: Id of the contact
        :type contact_id: int
        :param current_user: The user to retrieve contacts for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: A single contact
        :rtype: contact
        """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
        The route is intended for creating a contact

        :param body: The data for the contact to create
        :type body: ContactBase
        :param current_user: The user to retrieve contacts for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: Creates a contact through repository_contacts
        :rtype: contact
        """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
        The route is intended for updating a contact by id

        :param body: The data for the contact to update
        :type body: ContactUpdate
        :param contact_id: Id of the contact
        :type contact_id: int
        :param current_user: The user to retrieve contacts for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: Updates a contact through repository_contacts
        :rtype: contact
        """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
        The route is intended for deletion of a contact by id

        :param contact_id: Id of the contact
        :type contact_id: int
        :param current_user: The user to retrieve contacts for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: Deletes a contact through repository_contacts
        :rtype: contact
        """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/search/{credentials}", response_model=List[ContactResponse], name='Contacts by credentials')
async def search_contacts(credentials: str, db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    """
        The route is intended for search of a contact by credentials

        :param credentials: credentials of a contact
        :type credentials: int
        :param current_user: The user to retrieve contacts for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: Returns a searched contact
        :rtype: contact
        """
    contact = await repository_contacts.search_contacts(credentials, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/birthday/", response_model=List[ContactResponse], name='Upcoming birthdays')
async def upcoming_birthday(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
        The route is intended for search of a contacts with the upcoming birthdays
        in the future 7 days from current date.

        :param current_user: The user to retrieve contacts for
        :type current_user: User.
        :param db: The database session
        :type db: Session.
        :return: Returns a searched contacts
        :rtype: contact.
        """
    contact = await repository_contacts.upcoming_birthday(db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contact