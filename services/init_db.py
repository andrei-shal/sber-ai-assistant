"""Скрипт для создания SQLite БД payments.db и заполнения тестовыми данными."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "payments.db")

PAYMENTS_DATA = [
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "LANDLORD_DOWNTOWN_PLAZA", "amount": 12500.00, "status": "SUCCESS", "timestamp": 1764547200},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "SUPPLIER_RAW_MATERIALS", "amount": 25220.60, "status": "SUCCESS", "timestamp": 1765411200},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "UTILITY_CITY_POWER", "amount": 1134.82, "status": "SUCCESS", "timestamp": 1766275200},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "LANDLORD_DOWNTOWN_PLAZA", "amount": 12500.00, "status": "SUCCESS", "timestamp": 1767225600},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "LOGISTICS_FASTTRANS", "amount": 4885.95, "status": "SUCCESS", "timestamp": 1768435200},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "SUPPLIER_RAW_MATERIALS", "amount": 25940.15, "status": "SUCCESS", "timestamp": 1769644800},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "LANDLORD_DOWNTOWN_PLAZA", "amount": 12500.00, "status": "SUCCESS", "timestamp": 1769904000},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "UTILITY_CITY_POWER", "amount": 1176.28, "status": "SUCCESS", "timestamp": 1771113600},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "SUPPLIER_RAW_MATERIALS", "amount": 26485.70, "status": "SUCCESS", "timestamp": 1772323200},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "LANDLORD_DOWNTOWN_PLAZA", "amount": 12500.00, "status": "SUCCESS", "timestamp": 1775001600},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "SUPPLIER_RAW_MATERIALS", "amount": 27110.90, "status": "FAILED", "timestamp": 1777593600},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "SUPPLIER_RAW_MATERIALS", "amount": 27110.90, "status": "RETRYING", "timestamp": 1779408000},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "LANDLORD_DOWNTOWN_PLAZA", "amount": 12500.00, "status": "PENDING_APPROVAL", "timestamp": 1780272000},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "LOGISTICS_FASTTRANS", "amount": 5210.40, "status": "IN_PROGRESS", "timestamp": 1780704000},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "SOFTWARE_CLOUD_SERVICES", "amount": 3149.00, "status": "SCHEDULED", "timestamp": 1780963200},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "UTILITY_CITY_POWER", "amount": 1204.33, "status": "AWAITING_CONFIRMATION", "timestamp": 1781136000},
    {"company_id": "COMP_ACME_HOLDING", "receiver_id": "SUPPLIER_RAW_MATERIALS", "amount": 27895.45, "status": "IN_PROGRESS", "timestamp": 1781180000},
]


def init_db():
    """Создаёт таблицу payments и заполняет её тестовыми данными."""

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id   TEXT NOT NULL,
            receiver_id  TEXT NOT NULL,
            amount       REAL NOT NULL,
            status       TEXT NOT NULL,
            timestamp    INTEGER NOT NULL
        )
    """)

    cursor.executemany(
        "INSERT INTO payments (company_id, receiver_id, amount, status, timestamp) "
        "VALUES (:company_id, :receiver_id, :amount, :status, :timestamp)",
        PAYMENTS_DATA,
    )

    conn.commit()
    conn.close()
    print(f"БД создана: {DB_PATH}")
    print(f"Загружено записей: {len(PAYMENTS_DATA)}")


if __name__ == "__main__":
    init_db()