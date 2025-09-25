# db_manager.py
import os
from supabase import create_client
from dotenv import load_dotenv
# load environment variables
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")

supabase=create_client(url,key)
# ===================== Gymrats Table =====================

# Add Member
def add_member(name, phone, plan, start_date, end_date):
    return supabase.table("gymrats").insert({
        "name": name,
        "phone": phone,
        "plan": plan,
        "start_date": start_date,
        "end_date": end_date
    }).execute()

# Get All Members
def get_all_members():
    return supabase.table("gymrats").select("*").order("start_date").execute()

# Update Membership Plan
def update_member(member_id, new_plan, new_end_date):
    return supabase.table("gymrats").update({
        "plan": new_plan,
        "end_date": new_end_date
    }).eq("id", member_id).execute()  # Use "id" here

# Delete Member
def delete_member(member_id):
    return supabase.table("gymrats").delete().eq("id", member_id).execute()  # Use "id"

# ===================== Payments Table =====================

# Add Payment
def add_payment(gymrat_id, amount, payment_date=None, method=None):
    data = {
        "gymrat_id": gymrat_id,
        "amount": amount,
    }
    if payment_date:
        data["payment_date"] = payment_date
    if method:
        data["method"] = method
    return supabase.table("payments").insert(data).execute()

# Get All Payments
def get_all_payments():
    return supabase.table("payments").select("*").order("payment_date").execute()

# Get Payments for a Member
def get_payments_by_member(gymrat_id):
    return supabase.table("payments").select("*").eq("gymrat_id", gymrat_id).execute()

# Delete Payment Record
def delete_payment(payment_id):
    return supabase.table("payments").delete().eq("id", payment_id).execute()
