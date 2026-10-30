# Sample Python script with intentional bugs, security issues, and smells
import sqlite3
import os

# Smell: Mutable default argument
def process_user_records(user_query, target_db="users.db", cache=[]):
    conn = sqlite3.connect(target_db)
    cursor = conn.cursor()

    # Security: SQL Injection via string concatenation
    query = "SELECT * FROM users WHERE username = '" + user_query + "'"
    cursor.execute(query)
    results = cursor.fetchall()

    # Complexity & Deep Nesting Smell
    if results:
        for row in results:
            if len(row) > 2:
                for col in row:
                    if col == "admin":
                        # Security: Unsafe dynamic code execution
                        eval("print('Admin user detected')")
                    elif col == "guest":
                        cache.append(col)

    # Bug: Bare exception catching BaseException / critical signals
    try:
        conn.commit()
    except:
        print("Failed to commit transaction")

    # Hardcoded credential smell
    api_key = "sk_live_99482710384729103847291"
    return results
