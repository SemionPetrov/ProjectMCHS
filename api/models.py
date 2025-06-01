from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, Enum, Time, Text, SmallInteger
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

"""sqlalchemy and pydantic models"""


# Association tables for many-to-many relationships
employee_privileges = Table('employee_privileges', Base.metadata,
    Column('employee_id', Integer, ForeignKey('employee.id')),
    Column('privilege_id', Integer, ForeignKey('privilege.id'))
)

# Define the Privilege model
class Privilege(Base):
    __tablename__ = "privilege"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

# Define the Employee model
class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True)

    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)

    birthday = Column(Date, nullable=True)
    position_id = Column(Integer, ForeignKey('dolzhnost.id'))
    rank_id = Column(Integer, ForeignKey('rang.id'))
    
    # Relationships
    position = relationship("Dolzhnost", back_populates="employees")
    rank = relationship("Rang", back_populates="employees")
    privileges = relationship("Privilege", secondary=employee_privileges,
                           back_populates="employees")
    attestations = relationship("Attestation", back_populates="employee")
    exercises = relationship("Exercise", back_populates="employee")
    exercises_reports = relationship("ExercisesReport", back_populates="employee")
    1

# Define the Dolzhnost model
class Dolzhnost(Base):
    __tablename__ = "dolzhnost"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    group_position = Column(Enum('среднего и старшего начальствующего состава',
                               'рядового и младшего начальствующего состава',
                               'работников'), nullable=False)
    
    # Relationship
    employees = relationship("Employee", back_populates="position")

# Define the Rang model
class Rang(Base):
    __tablename__ = "rang"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    preparatory_period = Column(Time, nullable=False)
    
    # Relationship
    employees = relationship("Employee", back_populates="rank")

# Define the Attestation model
class Attestation(Base):
    __tablename__ = "attestation"
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    type_id = Column(Integer, ForeignKey('attestationtype.id'))
    status = Column(Integer, nullable=False)
    no_attestation_reason = Column(String(255))
    date = Column(Date, nullable=False)
    examination_date = Column(Date)
    
    # Relationships
    employee = relationship("Employee", back_populates="attestations")
    type = relationship("AttestationType")

# Define the AttestationType model
class AttestationType(Base):
    __tablename__ = "attestationtype"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

# Define the Exercise model
class Exercise(Base):
    __tablename__ = "exercise"
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    exercise_type_id = Column(Integer, ForeignKey('exercisetype.id'))
    date = Column(Date, nullable=False)
    address = Column(String(255), nullable=False)
    
    # Relationships
    employee = relationship("Employee", back_populates="exercises")
    type = relationship("ExerciseType")

# Define the ExerciseType model
class ExerciseType(Base):
    __tablename__ = "exercisetype"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

# Define the ExercisesReport model
class ExercisesReport(Base):
    __tablename__ = "exercisesreport"
    
    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    start_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)
    count_plan = Column(SmallInteger, nullable=False)
    count_actual = Column(SmallInteger, nullable=False)
    count_reason = Column(Enum('Отсутствие ХП-И', 'Отсутствие кислорода', 
                             'Отсутствие воздуха', 'Пожар', 'Запрет выездов', 'Прочее'),
                         nullable=False)
    comment = Column(Text)
    
    # Relationships
    exercise = relationship("Exercise")
    employee = relationship("Employee", back_populates="exercises_reports")

# Define the UserAuthentication model
class UserAuthentication(Base):
    __tablename__ = "userauthentication"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    token = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    
    # Relationship
    authentication_tokens = relationship("AuthenticationToken", back_populates="user")

# Define the AuthenticationToken model
class AuthenticationToken(Base):
    __tablename__ = "authenticationtokens"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('userauthentication.id'))
    token = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    
    # Relationship
    user = relationship("UserAuthentication", back_populates="authentication_tokens")
    
# Define the User model
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=True)
    login = Column(String(50), nullable=True)
    password_hash = Column(String(50), nullable=True)
    password_expiration = Column(DateTime, nullable=True)
    token = Column(String(50), nullable=True)
    employee = relationship("Employee")
