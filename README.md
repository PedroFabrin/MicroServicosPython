# Customer Queue API

A small REST API built with **FastAPI** to manage a customer service queue with **priority handling**, developed as a study project on APIs and services in Python.

Customers join either the **priority (P)** or the **normal (N)** queue. The API merges both queues, always serving priority customers first, and recalculates everyone's position as the queue moves.

## Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/fila` | List everyone waiting, in service order |
| `GET` | `/fila/{id}` | Get the customer at a given position |
| `POST` | `/fila` | Add a customer (`name`, `tipo`: `N` or `P`) |
| `PUT` | `/fila` | Call the next customer (priority first) |
| `DELETE` | `/fila/{id}` | Remove a customer from the queue |

### Example

```bash
curl -X POST http://localhost:8000/fila \
  -H "Content-Type: application/json" \
  -d '{"name": "Maria", "tipo": "P"}'
```

```json
{ "message": "Customer add successfully", "position": 1 }
```

## Tech stack

- Python
- FastAPI
- Pydantic for request validation

## Getting started

```bash
pip install fastapi uvicorn
cd EadToledo
uvicorn main:app --reload
```

Interactive docs available at **http://localhost:8000/docs**.

> Data is stored in memory, so the queue resets when the server restarts.

## Author

**Pedro Fabrin**, Backend Developer (Python, FastAPI, AI/LLMs)

[LinkedIn](https://www.linkedin.com/in/pedro-henrique-parizoto-fabrin-08765325b) · [GitHub](https://github.com/PedroFabrin)
