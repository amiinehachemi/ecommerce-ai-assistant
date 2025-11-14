from controllers.agent.agent import agent
import sqlite3, json

def seed_products():
    with open("products.json", "r") as f:
        products = json.load(f)

    conn = sqlite3.connect("products.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            stock INTEGER,
            warranty_days INTEGER,
            return_window_days INTEGER
        )
    """)

    for p in products:
        cur.execute("""
            INSERT INTO products (name, description, price, stock, warranty_days, return_window_days)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (p["name"], p["description"], p["price"], p["stock"], p["warranty_days"], p["return_window_days"]))

    conn.commit()
    conn.close()
    print("✅ Dummy products seeded successfully!")


def main():
    print("=== AI Terminal Chat ===")
    print("Type 'exit' or 'quit' to stop.\n")

    chat_history = []  # store all messages

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Add user message to history
        chat_history.append({"role": "user", "content": user_input})

        # Run the agent with full history
        reply = agent(chat_history)

        # Add AI reply to history
        chat_history.append({"role": "assistant", "content": reply})

        print(f"AI: {reply}\n")

if __name__ == "__main__":
    seed_products()
    main()
