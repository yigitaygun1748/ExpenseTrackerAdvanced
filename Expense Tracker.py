import json
from datetime import datetime
import turtle

# File names
EXPENSES_FILE = "expenses.json"
BUDGETS_FILE = "budgets.json"


def load_expenses():
    """Reads expenses from expenses.json and returns them as a list."""
    try:
        with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
            expense_list = json.load(file)
            return expense_list
    except FileNotFoundError:
        print("expenses.json file was not found. Empty expense list will be used.")
        return []
    except json.JSONDecodeError:
        print("expenses.json file format is invalid.")
        return []


def save_expenses(expense_list):
    """Saves the expense list into expenses.json."""
    try:
        with open(EXPENSES_FILE, "w", encoding="utf-8") as file:
            json.dump(expense_list, file, indent=4)
        print("Expenses were saved successfully.")
    except Exception as error:
        print("An error occurred while saving expenses:", error)


def load_budgets():
    """Reads budgets from budgets.json and returns them as a list."""
    try:
        with open(BUDGETS_FILE, "r", encoding="utf-8") as file:
            budget_list = json.load(file)
            return budget_list
    except FileNotFoundError:
        print("budgets.json file was not found. Empty budget list will be used.")
        return []
    except json.JSONDecodeError:
        print("budgets.json file format is invalid.")
        return []


def add_new_expense(expense_list):
    """Prompts the user for a new expense and adds it to the list."""
    print("\nStarting the process to add a new expense.")

    while True:
        new_expense_date = input("Please enter the date (YYYY-MM-DD): ")
        try:
            datetime.strptime(new_expense_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Invalid date format. Please enter the date in YYYY-MM-DD format.")

    while True:
        new_expense_amount = input("Please enter the amount of the expense: ")
        try:
            new_expense_amount = float(new_expense_amount)
            if new_expense_amount < 0:
                print("Error: Amount cannot be negative.")
            else:
                break
        except ValueError:
            print("Error: Invalid amount entered. Please try again.")

    new_expense_category = input("Please enter the category of the expense: ")
    new_expense_description = input("Please enter a description for the expense: ")

    new_expense = {
        "date": new_expense_date,
        "amount": new_expense_amount,
        "category": new_expense_category,
        "description": new_expense_description
    }

    expense_list.append(new_expense)

    expense_list.sort(key=lambda expense: expense["date"])

    save_expenses(expense_list)
    print("Expense successfully added.")


def view_all_expenses(expense_list):
    """Displays all expenses."""
    print("\nDisplaying all expenses:")

    if len(expense_list) == 0:
        print("No expenses found.")
        return

    for expense in expense_list:
        print(
            "Date: " + expense["date"] +
            ", Amount: " + str(expense["amount"]) +
            ", Category: " + expense["category"] +
            ", Description: " + expense["description"]
        )


def view_expenses_by_category(expense_list):
    """Displays expenses grouped by category."""
    print("\nGrouping expenses by category...")

    if len(expense_list) == 0:
        print("No expenses found.")
        return

    category_list = []

    for expense in expense_list:
        category = expense["category"]
        if category not in category_list:
            category_list.append(category)

    for category in category_list:
        print("\nCategory: " + category)

        for expense in expense_list:
            if expense["category"] == category:
                print(
                    "  Date: " + expense["date"] +
                    ", Amount: " + str(expense["amount"]) +
                    ", Description: " + expense["description"]
                )


def draw_a_bar(t, start_x, bar_width, height, value, category):
    """Draws a single bar on the bar chart in a cleaner way."""
    t.penup()
    t.goto(start_x, 0)
    t.setheading(0)
    t.pendown()

    t.fillcolor("red")
    t.begin_fill()

    t.left(90)
    t.forward(height)
    t.right(90)
    t.forward(bar_width)
    t.right(90)
    t.forward(height)
    t.left(90)

    t.end_fill()

    # value text above bar
    t.penup()
    t.goto(start_x + bar_width / 2, height + 15)
    t.pencolor("black")
    t.write("$" + str(round(value, 1)), align="center", font=("Arial", 10, "bold"))

    # category text below bar
    t.goto(start_x + bar_width / 2, -35)
    t.write(category, align="center", font=("Arial", 10, "normal"))

def generate_expense_bar_chart(expense_list):
    """Creates a more aesthetic bar chart showing total expenses by category."""
    print("\nGenerating Expense Bar Chart...")

    if len(expense_list) == 0:
        print("No expenses available to generate a bar chart.")
        return

    category_totals = {}

    for expense in expense_list:
        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    categories = list(category_totals.keys())
    values = list(category_totals.values())

    max_total = max(values)

    # chart settings
    bar_width = 70
    gap = 45
    left_margin = 50
    bottom_margin = 60
    top_margin = 80

    num_categories = len(categories)
    chart_width = left_margin + num_categories * (bar_width + gap)
    chart_height = 500

    # scale bars so they fit better visually
    usable_height = 350

    turtle.setup(width=1100, height=700)
    turtle.title("Expense Bar Chart")

    wn = turtle.Screen()
    wn.bgcolor("#f5f5f5")
    wn.setworldcoordinates(0, -80, chart_width, chart_height)

    ygt = turtle.Turtle()
    ygt.speed(0)
    ygt.hideturtle()
    ygt.pensize(2)

    # draw x-axis
    ygt.penup()
    ygt.goto(20, 0)
    ygt.pendown()
    ygt.goto(chart_width - 20, 0)

    start_x = left_margin

    for i in range(num_categories):
        category = categories[i]
        total = values[i]

        scaled_height = (total / max_total) * usable_height

        draw_a_bar(ygt, start_x, bar_width, scaled_height, total, category)
        start_x = start_x + bar_width + gap

    wn.exitonclick()

def budget_alerts(expense_list, budget_list):
    """Checks budgets and compares them with expenses."""
    print("\nChecking Budget Alerts...")

    if len(budget_list) == 0:
        print("No budgets available to check.")
        return

    for budget in budget_list:
        category = budget["category"]
        limit = budget["limit"]
        total_expenses = 0

        for expense in expense_list:
            if expense["category"] == category:
                total_expenses += expense["amount"]

        print("\nCategory: " + category)
        print("  Total Expenses: " + str(total_expenses))
        print("  Budget Limit: " + str(limit))

        if total_expenses > limit:
            print("  Alert: Expenses exceed the budget limit for " + category + ".")
        else:
            print("  Status: Expenses are within the budget for " + category + ".")


def search_expenses(expense_list):
    """Searches expenses by category or description."""
    print("\nStarting search operation...")

    keyword = input("Please enter a keyword to search (category or description): ").lower()
    matching_expenses = []

    for expense in expense_list:
        category = expense["category"].lower()
        description = expense["description"].lower()

        if keyword in category or keyword in description:
            matching_expenses.append(expense)

    print("Search operation completed.")

    if len(matching_expenses) > 0:
        print("\nMatching Expenses:")
        for expense in matching_expenses:
            print(
                "Date: " + expense["date"] +
                ", Amount: " + str(expense["amount"]) +
                ", Category: " + expense["category"] +
                ", Description: " + expense["description"]
            )
    else:
        print("No matching expenses found.")


def test_load_expenses():
    """Tests reading expenses.json."""
    expense_list = load_expenses()

    if len(expense_list) > 0:
        print("Test Passed: expenses.json data was read successfully.")
    else:
        print("Test Result: expenses.json is empty or could not be read.")


def test_load_budgets():
    """Tests reading budgets.json."""
    budget_list = load_budgets()

    if len(budget_list) > 0:
        print("Test Passed: budgets.json data was read successfully.")
    else:
        print("Test Result: budgets.json is empty or could not be read.")


def main():
    """Main menu of the program."""
    print("Reading expenses from expenses.json...")
    expense_list = load_expenses()

    print("Reading budgets from budgets.json...")
    budget_list = load_budgets()

    while True:
        print("\nMain Menu Options:")
        print("1. Add New Expense")
        print("2. View Expenses")
        print("3. Generate Bar Chart of Expenses")
        print("4. Search/Filter Expenses")
        print("5. Budget Alerts")
        print("6. Exit")

        choice = input("Please select an option: ")

        if choice == "1":
            add_new_expense(expense_list)

        elif choice == "2":
            while True:
                print("\nSelect an option:")
                print("a. View All Expenses")
                print("b. View Expenses by Category")
                print("c. Return to Main Menu")

                sub_choice = input("Please select an option: ")

                if sub_choice.lower() == "a":
                    view_all_expenses(expense_list)
                elif sub_choice.lower() == "b":
                    view_expenses_by_category(expense_list)
                elif sub_choice.lower() == "c":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3":
            generate_expense_bar_chart(expense_list)

        elif choice == "4":
            search_expenses(expense_list)

        elif choice == "5":
            budget_alerts(expense_list, budget_list)

        elif choice == "6":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    test_load_budgets()
    test_load_expenses()
    main()