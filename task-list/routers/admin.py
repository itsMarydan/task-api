from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from log import log
from db import get_db
from faker import Faker


# Initialize FastAPI app
router = APIRouter()

# seed database with data
@router.get("/admin/seed/", status_code=status.HTTP_201_CREATED)
def seed_data(db: Session = Depends(get_db)):
    log.info("Seeding database")
    for i in range(1, 200):
        fake = Faker()

        u =  schemas.UserBaseSchema(fname=fake.first_name(), lname=fake.last_name())
        new_user = models.UserEntity(**u.dict())
        db.add(new_user)
        db.commit()

        t =  schemas.TaskPostSchema(user_id=new_user.id,title=fake.text(20), description=fake.text(), completed=False, due_date=datetime.datetime.now())
        new_task = models.TaskEntity(**t.dict())
        db.add(new_task)
        db.commit()
    return {"status": "seeded users and tasks"}

# clear database
@router.delete("/admin/delete/", status_code=status.HTTP_200_OK)
def delete_data(db: Session = Depends(get_db)):
    log.info("Deleting all data")
    db.query(models.TaskEntity).delete()
    db.query(models.UserEntity).delete()
    db.commit()
    return {"status": "deleted all tasks and users"}