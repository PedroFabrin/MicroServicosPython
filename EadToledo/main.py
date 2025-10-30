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

priority_queue: List[Customer] = []
normal_queue: List[Customer] = []

def get_merged_queue() -> List[Customer]:
    merged = [c for c in priority_queue if not c.attended] + [c for c in normal_queue if not c.attended]
    for i, c in enumerate(merged, start=1):
        c.position = i
    return merged

@app.get("/fila", response_model=List[Customer])
def get_queue():
    return get_merged_queue()

@app.get("/fila/{id}", response_model=Customer)
def get_customer(id: int):
    merged = get_merged_queue()
    for c in merged:
        if not c.attended and c.position == id:
            return c
    raise HTTPException(status_code=404, detail="Customer not found.")

@app.post("/fila", response_model=dict)
def add_customer(customer: AddCustomer):
    if len(customer.name) == 0 or len(customer.name) > 20:
        raise HTTPException(status_code=404, detail="Name is mandatory and not longer than 20 characters.")
    if len(customer.tipo) != 1 or customer.tipo not in ['N', 'P']:
        raise HTTPException(status_code=400, detail="Field tipo only accept N (Normal), P (Prioritário)")

    new_customer = Customer(
        position=0,
        name=customer.name,
        arrival=datetime.now(),
        tipo=customer.tipo,
        attended=False
    )

    if customer.tipo == 'P':
        priority_queue.append(new_customer)
    else:
        normal_queue.append(new_customer)

    merged = get_merged_queue()
    next_position = len(merged)
    return {"message": "Customer add successfully", "position": next_position}

@app.put("/fila", response_model=dict)
def call_next_customer():
    if priority_queue and not priority_queue[0].attended:
        next_customer = priority_queue.pop(0)
        next_customer.attended = True
        next_customer.position = 0
        return {"message": "Priority customer called successfully"}
    if normal_queue and not normal_queue[0].attended:
        next_customer = normal_queue.pop(0)
        next_customer.attended = True
        next_customer.position = 0
        return {"message": "Normal customer called successfully"}
    return {"message": "Queue Empty"}

@app.delete("/fila/{id}", response_model=dict)
def delete_customer(id: int):
    merged = get_merged_queue()
    if id > len(merged) or id < 1:
        raise HTTPException(status_code=404, detail="Customer not found.")
    customer = merged[id - 1]
    if customer.tipo == 'P':
        priority_queue.remove(customer)
    else:
        normal_queue.remove(customer)

    return {"message": "Customer deleted successfully"}