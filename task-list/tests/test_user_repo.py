import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from repositories.user_repo import UserRepo
from models.models import UserEntity
from schemas.schemas import UserSchema
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

class TestUserRepo(unittest.TestCase):

    def setUp(self):
        # Create an in-memory SQLite database and session
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        _session = sessionmaker(bind=self.engine)
        self.session = _session()

        # add fake data to in memory db
        user_data = [UserEntity(fname='John', lname='Doe'),
                    UserEntity(fname='Jane', lname='Doe')]

        self.session.add_all(user_data)
        self.session.commit()

    def test_create_calls_db_add(self):
        # Set up
        mock_session = MagicMock()
        user_repo = UserRepo(db=mock_session)
        mock_user_schema_user = UserSchema(id=uuid4(), fname='John', lname='Doe')

        # Act
        result = user_repo.create(mock_user_schema_user)

        # Assert
        mock_session.add.assert_called_once()

    def test_create_calls_db_commit(self):
        # Set up
        mock_session = MagicMock()
        user_repo = UserRepo(db=mock_session)
        mock_user_schema_user = UserSchema(id=uuid4(), fname='John', lname='Doe')

        # Act
        result = user_repo.create(mock_user_schema_user)

        # Assert
        mock_session.commit.assert_called_once()

    def test_create_calls_db_refresh(self):
        # Set up
        mock_session = MagicMock()
        user_repo = UserRepo(db=mock_session)
        mock_user_schema_user = UserSchema(id=uuid4(), fname='John', lname='Doe')

        # Act
        result = user_repo.create(mock_user_schema_user)

        # Assert
        mock_session.refresh.assert_called_once()

    def test_create_returns_correct_type_user_entity(self):
        # Set up
        mock_session = MagicMock()
        user_repo = UserRepo(db=mock_session)
        mock_user_schema_user = UserSchema(id=uuid4(), fname='John', lname='Doe')

        # Act
        result = user_repo.create(mock_user_schema_user)

        # Assert
        self.assertIsInstance(result, UserEntity)

    def test_get_all_filters_by_fname(self):
        # Set up
        user_repo = UserRepo(db=self.session)

        # Act
        filtered_users_one = user_repo.get_all(search='John')
        filtered_users_none = user_repo.get_all(search='notfound')

        # Assert
        self.assertEqual(len(filtered_users_one), 1)
        self.assertEqual(len(filtered_users_none), 0)

if __name__ == '__main__':
    unittest.main()