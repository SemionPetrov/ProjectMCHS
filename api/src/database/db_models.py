from enum import unique
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, Enum, Time, Text, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime

from database.db_connector import Base
from config.db_timezone import prefered_timezone

"""
SQLalchemy models sourced by sqlalchemy
use alembic to migrade db after chages
"""


# Association tables for many-to-many relationships
user_privileges = Table('user_privileges', Base.metadata,
Column('user_id', 
       Integer, 
       ForeignKey(
           'user.id', 
            ondelete='CASCADE', 
            onupdate='CASCADE'
        ),
        primary_key=True
        ),
Column('privilege_id', 
       Integer, 
       ForeignKey(
           'privilege.id', 
           ondelete='RESTRICT', 
           onupdate='CASCADE'
        ),
        primary_key=True
    )
)

# Define the Privilege model
class Privilege(Base):
    __tablename__ = "privilege"
    
    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    name = Column(
        String(50), 
        nullable=False
    )
    
    # Relationships
    users = relationship(
        "User",
        secondary=user_privileges,
        back_populates="privileges",
        passive_deletes=True,
        passive_updates=True
    )


# Define the Employee model
class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    
    # personal info
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    surname = Column(String(50))
    birthday = Column(Date, nullable=True)
    
    # service info
    position_id = Column(
        Integer, 
        ForeignKey(
            'position.id',
            ondelete='RESTRICT', 
            onupdate='CASCADE'
        ),
        primary_key=True
    )
            
    rang_id = Column(
        Integer, 
        ForeignKey(
            'rang.id',
            ondelete='RESTRICT', 
            onupdate='CASCADE'
            ),
        primary_key=True
    )
    
    # whatever needs to be added
    comment = Column(Text)

    # Relationships
    position = relationship(
        "Position", 
        back_populates="employees"
    )
    rang = relationship(
        "Rang", 
        back_populates="employees"
    )
    attestations = relationship(
        "Attestation", 
        back_populates="employee",
        foreign_keys="[Attestation.employee_id]",
    )
    exercises = relationship(
        "PendingExercise", 
        back_populates="employee",
        foreign_keys="[PendingExercise.employee_id]"
    )


# Define the Position model
class Position(Base):
    __tablename__ = "position"

    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    name = Column(
        String(50), 
        nullable=False
    )

    group_position = Column(Enum(
            'среднего и старшего начальствующего состава',
            'рядового и младшего начальствующего состава',
            'работников'), 
        nullable=False
    )
    
    # Relationship
    employees = relationship(
        "Employee", 
        back_populates="position"
    )

# Define the Rang model
class Rang(Base):
    __tablename__ = "rang"
    
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    name = Column(
        String(50), 
        nullable=False
    )
    preparatory_period = Column(
        Time, 
        nullable=False
    )
    
    # Relationship
    employees = relationship(
        "Employee", 
        back_populates="rang",
        cascade="save-update"
    )

# Define the Attestation model
class Attestation(Base):
    __tablename__ = "attestation"
    
    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    employee_id = Column(
        Integer, 
        ForeignKey('employee.id', onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    type_id = Column(
        Integer, 
        ForeignKey('attestationtype.id', onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    status = Column(
        Integer, 
        nullable=False
    )
    no_attestation_reason = Column(
        String(255)
    )
    date = Column(
        Date, 
        nullable=False
    )
    examination_date = Column(
        Date
    )
    
    # Relationships
    employee = relationship(
        "Employee", 
        back_populates="attestations",
        foreign_keys="[Attestation.employee_id]"
    )
    type = relationship(
        "AttestationType"
    )

# Define the AttestationType model
class AttestationType(Base):
    __tablename__ = "attestationtype"
    
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    name = Column(
        String(50), 
        nullable=False
    )

# TODO rename to PENDING exercise
# Define the PendinExercise model
class PendingExercise(Base):
    __tablename__ = "exercise"
    
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    employee_id = Column(
        Integer, 
        ForeignKey('employee.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    exercise_type_id = Column(
        Integer, 
        ForeignKey('exercisetype.id', ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True
    )
    date = Column(
        DateTime, 
        nullable=False
    )
    address = Column(
        String(255), 
        nullable=False
    )
    
    comment = Column(
        String(255), 
        nullable=True
    )
    # Relationships
    employee = relationship(
        "Employee", 
        back_populates="exercises",
        foreign_keys="[PendingExercise.employee_id]"
    )
    type = relationship(
        "ExerciseType"
    )
    exercise_reports = relationship(
        "ExerciseReport",
        back_populates="exercise"
    ) 

# Define the ExerciseType model
class ExerciseType(Base):
    __tablename__ = "exercisetype"
    
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    name = Column(
        String(100), 
        nullable=False
    )

# Define the ExerciseReport model
class ExerciseReport(Base):
    __tablename__ = "exercisesreport"
    
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    exercise_id = Column(
        Integer, 
        ForeignKey('exercise.id', ondelete='RESTRICT', onupdate='CASCADE'),
        primary_key=True
    )
    start_date = Column(
        Date, 
        nullable=False
    )
    finish_date = Column(
        Date, 
        nullable=False
    )
    count_plan = Column(
        SmallInteger, 
        nullable=False
    )
    count_actual = Column(
        SmallInteger, 
        nullable=False
    )
    count_reason = Column(
        Enum(
            'Отсутствие ХП-И', 
            'Отсутствие кислорода', 
            'Отсутствие воздуха', 
            'Пожар', 
            'Запрет выездов', 
            'Прочее'),
        nullable=False
    )
    comment = Column(Text)
    
    # Relationships
    exercise = relationship(
            "PendingExercise",
            back_populates="exercise_reports"
    )


# Define the User model
class User(Base):
    __tablename__ = 'user'

    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    employee_id = Column(
        Integer, 
        ForeignKey('employee.id')
    )
    login = Column(
        String(50), 
        nullable=False,
        unique=True
    )
    contact_info = Column(
        String(100),
        nullable=True,
        unique=True
    )
    password_hash = Column(
        String(255), 
        nullable=False
    )
    password_expiration = Column(
        DateTime
    )
    created = Column(
        DateTime, 
        default=datetime.now(prefered_timezone),
        nullable=False
    )

    updated_at = Column(
        DateTime, 
        default=datetime.now(prefered_timezone), 
        onupdate=datetime.now(prefered_timezone),
        nullable=False
    )

    # Relationship
    employee = relationship("Employee")

    privileges = relationship(
        "Privilege",
        secondary = user_privileges,
        back_populates = "users",
        cascade = 'all, delete'
    )
