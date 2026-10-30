
from fastapi import FastAPI, HTTPException, status
from backend.schemas.customer import CustomerCreate, CustomerResponse

app = FastAPI(
    title="ClientFlow CRM API",
    description="Backend API for the ClientFlow CRM application.",
    version="0.2.0",
)


# Temporary in-memory storage
customers = []

# Temporary ID counter
next_customer_id = 1


# -----------------------------
# Basic application endpoints
# -----------------------------

@app.get("/")
def read_root():
    return {
        "message": "Welcome to ClientFlow CRM!",
        "status": "running",
    }


@app.get("/api/v1/welcome")
def welcome():
    return {
        "message": "Welcome to the ClientFlow CRM development journey!",
        "developer": "Bibek Baiju",
        "purpose": "Customer Relationship Management",
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "ClientFlow CRM API",
    }


@app.get("/api/v1/about")
def about():
    return {
        "name": "ClientFlow CRM",
        "description": "A customer relationship management application",
        "version": "0.2.0",
    }


@app.get("/api/v1/features")
def get_features():
    return {
        "features": [
            "Customer Management",
            "Sales Pipeline",
            "Task Management",
            "Customer Activity Tracking",
            "Sales Analytics",
        ]
    }


# -----------------------------
# Customer CRUD endpoints
# -----------------------------

@app.post(
    "/api/v1/customers",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(customer: CustomerCreate):

    global next_customer_id

    new_customer = {
        "id": next_customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "company": customer.company,
    }

    customers.append(new_customer)

    next_customer_id += 1

    return new_customer


@app.get("/api/v1/customers", response_model=list[CustomerResponse])
def get_customers():

    return customers


@app.get(
    "/api/v1/customers/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(customer_id: int):

    for customer in customers:
        if customer["id"] == customer_id:
            return customer

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Customer not found",
    )


@app.put(
    "/api/v1/customers/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(customer_id: int, updated_data: CustomerCreate):

    for customer in customers:

        if customer["id"] == customer_id:

            customer["name"] = updated_data.name
            customer["email"] = updated_data.email
            customer["phone"] = updated_data.phone
            customer["company"] = updated_data.company

            return customer

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Customer not found",
    )


@app.delete("/api/v1/customers/{customer_id}")
def delete_customer(customer_id: int):

    for index, customer in enumerate(customers):

        if customer["id"] == customer_id:

            customers.pop(index)

            return {
                "message": "Customer deleted successfully",
                "customer_id": customer_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Customer not found",
    )
