from datetime import date, timedelta
from typing import List
from sqlalchemy.orm import Session
from src.database.models import Contact


def get_upcoming_birthdays(db: Session) -> List[Contact]:
    today = date.today()
    contacts = db.query(Contact).all()
    upcoming = []

    for contact in contacts:
        if not contact.birthday:
            continue
        try:
            birthday_this_year = contact.birthday.replace(year=today.year)
        except ValueError:
            # Обробка 29 лютого для невисокосного року
            birthday_this_year = contact.birthday.replace(year=today.year, day=28)

        # Перевірка на перехід через Новий Рік
        if birthday_this_year < today:
            try:
                birthday_this_year = contact.birthday.replace(year=today.year + 1)
            except ValueError:
                birthday_this_year = contact.birthday.replace(
                    year=today.year + 1, day=28
                )

        delta_days = (birthday_this_year - today).days
        if 0 <= delta_days <= 7:
            upcoming.append(contact)

    return upcoming
