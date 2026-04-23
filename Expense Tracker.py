import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Files
expenses_file = "expenses.json"
budgets_file = "budgets.json"


# ---------------- FILE HANDLING ----------------

def load_data(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_data(expenses):
    try:
        with open(expenses_file, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=4)
    except:
        print("save error")


# ---------------- ADD EXPENSE ----------------

def add_expense(expenses):
    print("\nAdd expense")

    date = input("Date (YYYY-MM-DD): ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        print("Invalid date")
        return

    try:
        amount = float(input("Amount: "))
    except:
        print("Invalid amount")
        return

    category = input("Category: ")
    description = input("Description: ")

    expenses.append({
        "date": date,
        "amount": amount,
        "category": category,
        "description": description
    })

    save_data(expenses)
    print("Saved")


# ---------------- VIEW ----------------

def view(expenses):
    print("\nAll expenses")

    if not expenses:
        print("No data")
        return

    for e in expenses:
        print(
            e.get("date", "?"),
            e.get("amount", 0),
            e.get("category", "?"),
            e.get("description", "?")
        )


# ---------------- SEARCH ----------------

def search(expenses):
    print("\nSearch expenses")

    key = input("Keyword: ").lower()

    if not key:
        print("Empty input")
        return

    found = False

    for e in expenses:
        if key in e.get("category", "").lower() or key in e.get("description", "").lower():
            print(
                e.get("date"),
                e.get("amount"),
                e.get("category"),
                e.get("description")
            )
            found = True

    if not found:
        print("No results")


# ---------------- CHARTS ----------------

def get_totals(expenses):
    totals = defaultdict(float)

    for e in expenses:
        try:
            totals[e.get("category", "Unknown")] += float(e.get("amount", 0))
        except:
            pass

    return totals


def bar_chart(expenses):
    print("\nGenerating Bar Chart...")

    data = get_totals(expenses)

    if not data:
        print("No data")
        return

    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color="skyblue")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1f}",
            ha="center",
            va="bottom"
        )

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")

    plt.show()


def pie_chart(expenses):
    print("\nGenerating Pie Chart...")

    data = get_totals(expenses)

    if not data:
        print("No data")
        return

    plt.figure(figsize=(7, 7))

    plt.pie(
        data.values(),
        labels=data.keys(),
        autopct="%1.1f%%",
        startangle=140
    )

    plt.title("Expense Distribution")
    plt.tight_layout()

    plt.show()


# ---------------- BUDGET ----------------

def budget_check(expenses, budgets):
    print("\nBudget check")

    if not budgets:
        print("No budgets")
        return

    for b in budgets:

        category = str(b.get("category", "")).strip().lower()

        try:
            limit = float(b.get("limit", 0))
        except:
            continue

        total = 0

        for e in expenses:
            if str(e.get("category", "")).strip().lower() == category:
                try:
                    total += float(e.get("amount", 0))
                except:
                    pass

        print("\nCategory:", category)
        print("Spent:", total)
        print("Limit:", limit)

        if total > limit:
            print("OVER BUDGET")
        else:
            print("OK")


# ---------------- MENU ----------------

def menu():
    print("\n========================")
    print("   EXPENSE TRACKER")
    print("========================")
    print("1 - Add a new expense")
    print("2 - View all expenses")
    print("3 - Show bar chart")
    print("4 - Show pie chart")
    print("5 - Search expenses")
    print("6 - Check budget")
    print("7 - Exit")


# ---------------- MAIN ----------------

def main():
    expenses = load_data(expenses_file)
    budgets = load_data(budgets_file)

    while True:
        menu()
        choice = input("Select: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view(expenses)

        elif choice == "3":
            bar_chart(expenses)

        elif choice == "4":
            pie_chart(expenses)

        elif choice == "5":
            search(expenses)

        elif choice == "6":
            budget_check(expenses, budgets)

        elif choice == "7":
            print("Bye 👋")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
