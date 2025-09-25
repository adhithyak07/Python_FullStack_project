#src logic.py

from src.db import DatabaseManager
from datetime import date, datetime

class Gym_membership_system:
   """"
   Acts as a bridge b.1 frontend (streamlit/FastAPI) and the database.
   """
   def __init__(self):
      # create a database manages instance(this will handles actual db operations)
      self.db=DatabaseManager()
# ---create -----------
# ===================== Gymrat Manager =====================
class GymratManager:
    """
    Handles all operations related to gym members.
    """

    def __init__(self):
        self.db = DatabaseManager()

    def add_member(self, name: str, phone: str, plan: str, start_date: date = None, end_date: date = None):
        if not start_date:
            start_date = date.today()
        result = self.db.add_member(name=name, phone=phone, plan=plan, start_date=start_date, end_date=end_date)
        if result:
            return {"success": True, "message": f"Member '{name}' added successfully.", "data": result}
        return {"success": False, "message": f"Failed to add member '{name}'."}

    def get_all_members(self):
        result = self.db.get_all_members()
        if result:
            return {"success": True, "data": result, "message": "Fetched all members successfully."}
        return {"success": False, "message": "Failed to fetch members."}

    def update_member(self, member_id: str, new_plan: str, new_end_date: date):
        result = self.db.update_member(member_id=member_id, new_plan=new_plan, new_end_date=new_end_date)
        if result:
            return {"success": True, "message": f"Member '{member_id}' updated successfully.", "data": result}
        return {"success": False, "message": f"Failed to update member '{member_id}'."}

    def delete_member(self, member_id: str):
        result = self.db.delete_member(member_id=member_id)
        if result:
            return {"success": True, "message": f"Member '{member_id}' deleted successfully.", "data": result}
        return {"success": False, "message": f"Failed to delete member '{member_id}'."}


# ===================== Payment Manager =====================
class PaymentManager:
    """
    Handles all operations related to payments.
    """

    def __init__(self):
        self.db = DatabaseManager()

    def add_payment(self, gymrat_id: str, amount: float, payment_date: datetime = None, method: str = None):
        result = self.db.add_payment(gymrat_id=gymrat_id, amount=amount, payment_date=payment_date, method=method)
        if result:
            return {"success": True, "message": f"Payment of {amount} added for member '{gymrat_id}'.", "data": result}
        return {"success": False, "message": f"Failed to add payment for member '{gymrat_id}'."}

    def get_all_payments(self):
        result = self.db.get_all_payments()
        if result:
            return {"success": True, "data": result, "message": "Fetched all payments successfully."}
        return {"success": False, "message": "Failed to fetch payments."}

    def get_payments_by_member(self, gymrat_id: str):
        result = self.db.get_payments_by_member(gymrat_id=gymrat_id)
        if result:
            return {"success": True, "data": result, "message": f"Fetched payments for member '{gymrat_id}' successfully."}
        return {"success": False, "message": f"Failed to fetch payments for member '{gymrat_id}'."}

    def delete_payment(self, payment_id: int):
        result = self.db.delete_payment(payment_id=payment_id)
        if result:
            return {"success": True, "message": f"Payment '{payment_id}' deleted successfully.", "data": result}
        return {"success": False, "message": f"Failed to delete payment '{payment_id}'."}