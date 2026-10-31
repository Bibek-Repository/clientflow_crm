from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.session import engine, Base, get_db
from backend.models.customer import Customer
from backend.schemas.customer import CustomerCreate, CustomerResponse

from fastapi.middleware.cors import CORSMiddleware


# Create database tables when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


# Initialize FastAPI
app = FastAPI(
    title="ClientFlow CRM API",
    description="Backend API for the ClientFlow CRM application.",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Basic routes
@app.get("/")
def home():
    return {"message": "Welcome to ClientFlow CRM API"}


@app.get("/api/v1/welcome")
def welcome():
    return {"message": "Welcome to ClientFlow CRM!"}


@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/v1/about")
def about():
    return {
        "project": "ClientFlow CRM",
        "version": "0.3.0",
        "description": "A customer relationship management system",
    }


@app.get("/api/v1/features")
def features():
    return {
        "features": [
            "Customer Management",
            "Sales Pipeline",
            "Task Management",
            "Activity Tracking",
        ]
    }


# CREATE CUSTOMER
@app.post(
    "/api/v1/customers",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
):

    existing_customer = db.scalar(
        select(Customer).where(
            Customer.email == str(customer.email)
        )
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A customer with this email already exists",
        )

    new_customer = Customer(
        name=customer.name,
        email=str(customer.email),
        phone=customer.phone,
        company=customer.company,
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# GET ALL CUSTOMERS
@app.get(
    "/api/v1/customers",
    response_model=list[CustomerResponse],
)
def get_customers(db: Session = Depends(get_db)):

    statement = select(Customer).order_by(Customer.id)

    customers = db.scalars(statement).all()

    return customers


# GET CUSTOMER BY ID
@app.get(
    "/api/v1/customers/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):

    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


# UPDATE CUSTOMER
@app.put(
    "/api/v1/customers/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    updated_data: CustomerCreate,
    db: Session = Depends(get_db),
):

    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    existing_customer = db.scalar(
        select(Customer).where(
            Customer.email == str(updated_data.email),
            Customer.id != customer_id,
        )
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already used by another customer",
        )

    customer.name = updated_data.name
    customer.email = str(updated_data.email)
    customer.phone = updated_data.phone
    customer.company = updated_data.company

    db.commit()
    db.refresh(customer)

    return customer


# DELETE CUSTOMER
@app.delete("/api/v1/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):

    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully",
        "customer_id": customer_id,
    }