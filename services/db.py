import sqlite3
import os

_DB_PATH = os.path.join(os.path.dirname(__file__), "payments.db")

# --- Data source: SQLite ---

def query_payments(sql_query: str) -> list[dict]:
    """Выполняет произвольный SQL SELECT и возвращает список платежей.

    Колонки в результате: id, company_id, receiver_id, amount, status, timestamp.
    """
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


# --- Legacy stub (hardcoded data) ---

def get_user_payments():
    return [
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "LANDLORD_DOWNTOWN_PLAZA",
    "amount": 12500.00,
    "status": "SUCCESS",
    "timestamp": 1764547200
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "SUPPLIER_RAW_MATERIALS",
    "amount": 25220.60,
    "status": "SUCCESS",
    "timestamp": 1765411200
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "UTILITY_CITY_POWER",
    "amount": 1134.82,
    "status": "SUCCESS",
    "timestamp": 1766275200
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "LANDLORD_DOWNTOWN_PLAZA",
    "amount": 12500.00,
    "status": "SUCCESS",
    "timestamp": 1767225600
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "LOGISTICS_FASTTRANS",
    "amount": 4885.95,
    "status": "SUCCESS",
    "timestamp": 1768435200
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "SUPPLIER_RAW_MATERIALS",
    "amount": 25940.15,
    "status": "SUCCESS",
    "timestamp": 1769644800
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "LANDLORD_DOWNTOWN_PLAZA",
    "amount": 12500.00,
    "status": "SUCCESS",
    "timestamp": 1769904000
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "UTILITY_CITY_POWER",
    "amount": 1176.28,
    "status": "SUCCESS",
    "timestamp": 1771113600
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "SUPPLIER_RAW_MATERIALS",
    "amount": 26485.70,
    "status": "SUCCESS",
    "timestamp": 1772323200
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "LANDLORD_DOWNTOWN_PLAZA",
    "amount": 12500.00,
    "status": "SUCCESS",
    "timestamp": 1775001600
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "SUPPLIER_RAW_MATERIALS",
    "amount": 27110.90,
    "status": "FAILED",
    "timestamp": 1777593600
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "SUPPLIER_RAW_MATERIALS",
    "amount": 27110.90,
    "status": "RETRYING",
    "timestamp": 1779408000
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "LANDLORD_DOWNTOWN_PLAZA",
    "amount": 12500.00,
    "status": "PENDING_APPROVAL",
    "timestamp": 1780272000
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "LOGISTICS_FASTTRANS",
    "amount": 5210.40,
    "status": "IN_PROGRESS",
    "timestamp": 1780704000
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "SOFTWARE_CLOUD_SERVICES",
    "amount": 3149.00,
    "status": "SCHEDULED",
    "timestamp": 1780963200
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "UTILITY_CITY_POWER",
    "amount": 1204.33,
    "status": "AWAITING_CONFIRMATION",
    "timestamp": 1781136000
  },
  {
    "company_id": "COMP_ACME_HOLDING",
    "receiver_id": "SUPPLIER_RAW_MATERIALS",
    "amount": 27895.45,
    "status": "IN_PROGRESS",
    "timestamp": 1781180000
  }
]

print(query_payments(""))