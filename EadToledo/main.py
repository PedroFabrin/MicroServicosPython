from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI()

class Customer(BaseModel):
    position: int
    name: str
    arrival: datetime
    tipo: str
    attended: bool = False

class AddCustomer(BaseModel):
    name: str
    tipo: str

queue: List[Customer] = []

@app.get("/fila", response_model=List[Customer])
def get_queue():
    return [c for c in queue if not c.attended]

@app.get("/fila/{id}", response_model=Customer)
def get_customer(id: int):
    for c in queue:
        if not c.attended and c.position == id:
            return c
    raise HTTPException(status_code=404, detail="Customer not found.")

@app.post("/fila", response_model=dict)
def add_customer(customer: AddCustomer):
    if len(customer.name) == 0:
        raise HTTPException(status_code=404, detail="Name is mandatory")
    if len(customer.tipo) != 1 or customer.tipo not in ['N', 'P']:
        raise HTTPException(status_code=400, detail="Field tipo only accept N (Normal), P (Prioritário)")

    queue_count = len([c for c in queue if not c.attended])
    next_position = queue_count + 1

    new_customer = Customer(
        position=next_position,
        name=customer.name,
        arrival=datetime.now(),
        tipo=customer.tipo,
        attended=False
    )

    queue.append(new_customer)
    return {"message": "Customer add successfully", "position": next_position}

@app.put("/fila", response_model=dict)
def call_next_customer():
    first_customer = None
    for c in queue:
        if not c.attended and c.position == 1:
            first_customer = c
            break

    if first_customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")

    first_customer.position = 0
    first_customer.attended = True

    for c in queue:
        if not c.attended and c.position > 1:
            c.position -= 1
    return {"message": "Next customer called successfully"}

@app.delete("/fila/{id}", response_model=dict)
def delete_customer(id: int):
    customer_to_remove = None
    for c in queue:
        if not c.attended and c.position == id:
            customer_to_remove = c
            break

    if customer_to_remove is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")

    queue.remove(customer_to_remove)

    for c in queue:
        if not c.attended and c.position > id:
            c.position -= 1

    return {"message": "Customer deleted successfully"}