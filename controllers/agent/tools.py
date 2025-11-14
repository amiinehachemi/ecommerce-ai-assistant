import re
import json
import sqlite3
import traceback
import difflib
from langchain.tools import tool
    
@tool
def list_products() -> str:
    """Read and list all products from the local SQLite database."""
    conn = sqlite3.connect("products.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM products").fetchall()
    conn.close()

    if not rows:
        return "No products found in the catalog."

    summary = [
        f"{r['id']}: {r['name']} (${r['price']}) — Stock: {r['stock']}"
        for r in rows
    ]
    return "\n".join(summary)


def get_orders_by_contact(contact_name: str) -> str:
    """
    Retrieve all orders associated with a contact name.
    The search is case-insensitive and works with partial or full names (e.g. 'sarah', 'john doe', 'mary ann').
    Returns a summary of each order with items, total, and status.
    """

    print(f"🔍 Searching orders for contact name: {contact_name}")

    conn = sqlite3.connect("orders.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Normalize input (lowercase, trim spaces)
    normalized_name = contact_name.strip().lower()

    # Search for partial matches
    rows = cur.execute("""
        SELECT * FROM orders
        WHERE LOWER(contact_name) LIKE ?
        ORDER BY created_at DESC
    """, (f"%{normalized_name}%",)).fetchall()

    conn.close()

    if not rows:
        return f"❌ No orders found for '{contact_name}'."

    # Build readable summaries
    summaries = []
    for row in rows:
        try:
            items = json.loads(row["items_json"])
        except Exception:
            items = []

        item_lines = "\n".join(
            [f"- {i['name']} x{i['quantity']} (${i['price_each']} ea)" for i in items]
        ) or "No items listed."

        summary = (
            f"🧾 Order ID: {row['id']}\n"
            f"Name: {row['contact_name']}\n"
            f"Status: {row['status']}\n"
            f"Total: ${row['total']}\n"
            f"Date: {row['created_at']}\n"
            f"Items:\n{item_lines}\n"
            "----------------------"
        )
        summaries.append(summary)

    return "\n\n".join(summaries)


@tool
def create_order_quote(user_id: str, contact_name: str, request: str) -> str:
    """
    Use this tool when the user wants to buy or order one or more products by name.
    The user may mention incomplete or misspelled product names.
    Before calling this tool, make sure you have the contact name.
    saves the order in orders.db.
    """
    print("=== [LOG] create_order_quote triggered ===")
    print(f"User ID: {user_id}, Contact: {contact_name}, Request: {request}")

    conn_prod = None
    conn_order = None

    try:
        # Connect to product DB
        conn_prod = sqlite3.connect("products.db")
        conn_prod.row_factory = sqlite3.Row
        cur = conn_prod.cursor()
        products = cur.execute("SELECT * FROM products").fetchall()
        if not products:
            return "❌ No products found in catalog."

        all_names = [p["name"].lower() for p in products]
        words = re.findall(r"[a-zA-Z]+", request.lower())

        matched_items = []
        total_price = 0.0
        request_text = request.lower()

        for name in all_names:
            ratio = difflib.SequenceMatcher(None, name, request_text).ratio()
            if ratio >= 0.4:
                product = next((p for p in products if p["name"].lower() == name), None)
                if product:
                    matched_items.append({
                        "name": product["name"],
                        "price_each": product["price"],
                        "quantity": 1,
                        "subtotal": product["price"]
                    })
                    total_price += product["price"]

        if not matched_items:
            for word in words:
                close = difflib.get_close_matches(word, all_names, n=1, cutoff=0.5)
                if close:
                    product = next((p for p in products if p["name"].lower() == close[0]), None)
                    if product and product not in matched_items:
                        matched_items.append({
                            "name": product["name"],
                            "price_each": product["price"],
                            "quantity": 1,
                            "subtotal": product["price"]
                        })
                        total_price += product["price"]

        if not matched_items:
            return "❌ I couldn’t find any products close to what you mentioned."

        # Connect to order DB
        conn_order = sqlite3.connect("orders.db")
        cur_order = conn_order.cursor()
        cur_order.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                contact_name TEXT,
                items_json TEXT,
                total REAL,
                status TEXT DEFAULT 'quote',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur_order.execute(
            "INSERT INTO orders (user_id, contact_name, items_json, total) VALUES (?, ?, ?, ?)",
            (user_id, contact_name.strip().lower(), json.dumps(matched_items), total_price)
        )
        conn_order.commit()
        order_id = cur_order.lastrowid

        summary_lines = [f"- {i['name']} x{i['quantity']} @ ${i['price_each']}" for i in matched_items]
        summary_text = "\n".join(summary_lines)

        return (
            f"🧾 Order Quote #{order_id}\n"
            f"Name: {contact_name}\n"
            f"Customer ID: {user_id}\n"
            f"Items:\n{summary_text}\n"
            f"Total: ${round(total_price, 2)}"
        )

    except Exception as e:
        print("[ERROR] Exception in create_order_quote:")
        traceback.print_exc()
        return f"❌ Failed to create order quote: {str(e)}"

    finally:
        if conn_prod:
            conn_prod.close()
        if conn_order:
            conn_order.close()
        print("=== [LOG] create_order_quote finished ===\n")