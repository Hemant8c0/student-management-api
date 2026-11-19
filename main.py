from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from sqlalchemy import String, Integer, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    course: Mapped[str] = mapped_column(String(100), nullable=False)


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=16, le=100)
    course: str = Field(min_length=2, max_length=100)


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=16, le=100)
    course: str | None = Field(default=None, min_length=2, max_length=100)


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    course: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Management API",
    description="CRUD API using FastAPI, SQLAlchemy and SQLite",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "Student Management API is running", "docs": "/docs"}


@app.post("/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Annotated[Session, Depends(get_db)]):
    existing = db.scalar(select(Student).where(Student.email == str(payload.email)))
    if existing:
        raise HTTPException(status_code=400, detail="A student with this email already exists")

    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/students/", response_model=list[StudentResponse])
def get_students(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(Student).order_by(Student.id)).all()


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Annotated[Session, Depends(get_db)]):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, payload: StudentUpdate, db: Annotated[Session, Depends(get_db)]):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    updates = payload.model_dump(exclude_unset=True)
    if "email" in updates and updates["email"] is not None:
        updates["email"] = str(updates["email"])
        duplicate = db.scalar(
            select(Student).where(Student.email == updates["email"], Student.id != student_id)
        )
        if duplicate:
            raise HTTPException(status_code=400, detail="Another student already uses this email")

    for field, value in updates.items():
        if value is not None:
            setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int, db: Annotated[Session, Depends(get_db)]):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted successfully"}
