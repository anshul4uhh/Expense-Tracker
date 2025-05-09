from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Body
from datetime import date
from typing import List
from pydantic import BaseModel
import db_helper


class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/debug/expenses")
def debug_all_expenses():
    return db_helper.fetch_all_data()


@app.get("/expenses/{expense_date}", response_model= List[Expense])
def get_expense(expense_date:date):
    expenses = db_helper.fetch_expense_by_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500,detail="failed to retrieve expense summary from database")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense] = Body(...)):
    if not expenses:
        raise HTTPException(status_code=400, detail="No expense data provided.")

    db_helper.delete_expense_by_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expense Updated Successfully"}


@app.post("/analytics")
def get_analysis(date_range: DateRange = Body(...)):
    data = db_helper.fetch_expense_summary(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500,detail="failed to retrieve expense summary from database")
    total = sum([row['total'] for row in data])
    breakdown={}
    for row in data:
        percentage = (row['total']/total)*100 if total !=0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown

@app.post("/analyticsmonth")
def get_analysis_month(date_range: DateRange = Body(...)):
    data = db_helper.fetch_expense_summary_month(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500,detail="failed to retrieve expense summary from database")
    return data

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
