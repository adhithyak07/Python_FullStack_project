# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Add src folder to path to import managers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import GymratManager, PaymentManager

# -------------------------- App Setup --------------------------
app = FastAPI(title="Gym Membership System API", version="1.0")

# -------------------------- Allow frontend (CORS) --------------------------


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------- Pydantic Models --------------------------
class Member(BaseModel):
    name: str
    phone: str
    plan: str
    end_date: str  # YYYY-MM-DD

class Payment(BaseModel):
    gymrat_id: str
    amount: float
    method: str = None

# -------------------------- Manager Instances --------------------------
gymrat_mgr = GymratManager()
payment_mgr = PaymentManager()

# -------------------------- Gym Member Routes --------------------------
@app.post("/members/")
def add_member(member: Member):
    """
    Add a new gym member
    """
    result = gymrat_mgr.add_member(
        name=member.name,
        phone=member.phone,
        plan=member.plan,
        end_date=member.end_date
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/members/")
def get_members():
    result = gymrat_mgr.get_all_members()
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.put("/members/{member_id}")
def update_member(member_id: str, member: Member):
    result = gymrat_mgr.update_member(
        member_id=member_id,
        new_plan=member.plan,
        new_end_date=member.end_date
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/members/{member_id}")
def delete_member(member_id: str):
    result = gymrat_mgr.delete_member(member_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# -------------------------- Payment Routes --------------------------
@app.post("/payments/")
def add_payment(payment: Payment):
    result = payment_mgr.add_payment(
        gymrat_id=payment.gymrat_id,
        amount=payment.amount,
        method=payment.method
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/payments/")
def get_all_payments():
    result = payment_mgr.get_all_payments()
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/payments/{gymrat_id}")
def get_payments_by_member(gymrat_id: str):
    result = payment_mgr.get_payments_by_member(gymrat_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    result = payment_mgr.delete_payment(payment_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# -------------------------- Run Main --------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
