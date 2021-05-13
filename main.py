import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi import Response, status
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional

app = FastAPI()

class Supplier(BaseModel):
    id: int
    name: str

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific 


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

@app.get("/suppliers")
async def get_suppliers(response: Response):
    app.db_connection.row_factory = sqlite3.Row
    suppliers = app.db_connection.execute("SELECT SupplierID, CompanyName FROM Suppliers ORDER BY SupplierID").fetchall()
    response.status_code = status.HTTP_200_OK
    return suppliers

@app.get("/suppliers/{id}")
async def get_suppliers_id(response: Response, id: int):
    app.db_connection.row_factory = sqlite3.Row
    check_id = app.db_connection.execute(f"SELECT COUNT(*) as count FROM Suppliers WHERE SupplierID = {id}").fetchone()
    #return check_id
    if check_id['count'] == 0:
        raise HTTPException(status_code=404)
    else:
        suppliers_id = app.db_connection.execute(f"SELECT * FROM Suppliers WHERE SupplierID = {id} ").fetchone()
        response.status_code = status.HTTP_200_OK
    return suppliers_id
