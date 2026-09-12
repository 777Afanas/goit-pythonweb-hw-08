from typing import Optional, List
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contact_by_email(db: Session, email: str) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.email == email).first()


def get_contact_by_id(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_all_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


def search_contacts(
    db: Session,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
) -> List[Contact]:
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()


def update_contact(
    db: Session, contact_id: int, body: ContactUpdate
) -> Optional[Contact]:
    contact = get_contact_by_id(db, contact_id)
    if not contact:
        return None
    for key, value in body.model_dump().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int) -> Optional[Contact]:
    contact = get_contact_by_id(db, contact_id)
    if not contact:
        return None
    db.delete(contact)
    db.commit()
    return contact
