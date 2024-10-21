import matplotlib.pyplot as plt

class Frame:
    def __init__(self, name, attributes=None):
        self.name = name
        self.attributes = attributes if attributes else {}

    def get(self, attribute):
        return self.attributes.get(attribute, None)

    def set(self, attribute, value):
        self.attributes[attribute] = value

    def increment(self, attribute, value):
        self.attributes[attribute] = self.attributes.get(attribute, 0) + value


class ExpenseManager:
    def __init__(self):
        self.money = 0
        self.frames = {}  

    def add_income(self, amount):
        if amount < 0:
            print("Error: Income cannot be negative.")
            return
        self.money += amount
        print(f"Income increased by {amount}. Total balance: {self.money}")

    def show_income(self):
        print(f"Your remaining balance is: {self.money}")

    def add_Category(self, category, total_limited_amount):
        if total_limited_amount < 0:
            print("Error: Budget limit must be a positive value.")
            return

        if category not in self.frames:
            self.frames[category] = Frame(category, {"total_limited_amount": total_limited_amount, "expense": {}, "amount": 0})
            print(f"Category '{category}' added with a budget of {total_limited_amount}.")
        else:
            print("This category already exists.")

    def add_expense(self, category, expense, amount_expense):
        if amount_expense < 0:
            print("Error: Expense amount cannot be negative.")
            return
        
        if category in self.frames:
            if self.money >= amount_expense:
                previous_total_amount = self.frames[category].attributes["amount"]
                self.frames[category].attributes["amount"] = previous_total_amount + amount_expense

                if expense not in self.frames[category].attributes.get("expense", {}):
                    self.frames[category].attributes["expense"][expense] = {"expense_amount": amount_expense}
                else:
                    previous_amount = self.frames[category].attributes["expense"][expense]["expense_amount"]
                    new_total = previous_amount + amount_expense
                    self.frames[category].attributes["expense"][expense]["expense_amount"] = new_total

                self.money -= amount_expense
                print(f"Your remaining balance is '{self.money}'.")
                print(f"You expensed '{amount_expense}' for '{expense}'. Now the total expense for this category is '{self.frames[category].attributes['amount']}'.")
            else:
                print(f"Insufficient funds! You only have '{self.money}', but you're trying to expense '{amount_expense}'.")
        else:
            print("Sorry, we don't have this category.")

    def Show_Report(self):
        print("\n--- Expense Report ---")
        print(f"Remaining Balance: {self.money}")
        print("Categories:")
        
        for category, frame in self.frames.items():
            expense_amount = frame.get("amount")
            budget_limit = frame.get("total_limited_amount")
            status = "Within Budget" if expense_amount <= budget_limit else "Exceeded Budget"
            print(f"  {category}:")
            print(f"    - Total Expenses: {expense_amount}")
            print(f"    - Budget Limit: {budget_limit}")
            print(f"    - Status: {status}")
            
            expenses = frame.attributes.get("expense", {})
            for sub_cat, sub_info in expenses.items():
                print(f"      - {sub_cat}: {sub_info['expense_amount']}")

        print("-----------------------")

    def set_budget(self, category, limit):
        if limit < 0:
            print("Error: Budget limit must be positive.")
            return
        
        if category not in self.frames:
            self.frames[category] = Frame(category, {"amount": 0})
        self.frames[category].set("total_limited_amount", limit)
        print(f"Budget for {category} set at {limit}.")

    def check_budget(self):
        print("\nBudget Check:")
        for category, frame in self.frames.items():
            budget_limit = frame.get("total_limited_amount")
            expense_amount = frame.get("amount")
            if budget_limit is not None:
                if expense_amount > budget_limit:
                    print(f"Warning: {category} exceeded the budget. Spent: {expense_amount}, Budget: {budget_limit}")
                else:
                    print(f"{category} is within budget. Spent: {expense_amount}, Budget: {budget_limit}")

    def visualize_expenses(self):
        categories = []
        expenses = []
        for category, frame in self.frames.items():
            amount = frame.get("amount")
            if amount > 0:
                expenses.append(amount)
                categories.append(category)
        
        if categories and expenses:
            plt.bar(categories, expenses, color='blue')
            plt.title("Expense Breakdown")
            plt.xlabel("Category/Subcategory")
            plt.ylabel("Amount")
            plt.xticks(rotation=45, ha="right")
            plt.show()
        else:
            print("No expenses to display.")


if __name__ == "__main__":
    manager = ExpenseManager()

    running = True
    while running:
        print("\nOptions:")
        print("0. Add your money")
        print("1. Know your money")
        print("2. Add category")
        print("3. Add expense")
        print("4. Set budget")
        print("5. Check budget")
        print("6. Visualize expenses")
        print("7. Show report")
        print("8. Exit")
        
        choice = input("Enter choice: ")

        if choice == '0':
            try:
                amount = int(input("Enter money amount: "))
                manager.add_income(amount)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == '1':
            manager.show_income()

        elif choice == '2':
            category = input("Enter category name: ")
            try:
                total_limited_amount = int(input("Enter total budget amount: "))
                manager.add_Category(category, total_limited_amount)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == '3':
            category = input("Enter category name for expense: ")
            subCategory = input("Enter expense name: ")
            try:
                amount_expense = int(input("Amount expense: "))
                manager.add_expense(category, subCategory, amount_expense)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == '4':
            category = input("Enter category name to set budget: ")
            try:
                limit = int(input("Enter the budget limit: "))
                manager.set_budget(category, limit)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == '5':
            manager.check_budget()

        elif choice == '6':
            manager.visualize_expenses()

        elif choice == '7':
            manager.Show_Report()

        elif choice == '8':
            print("Exiting...")
            running = False

        else:
            print("Invalid choice. Please try again.")
