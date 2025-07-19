import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class ExpenseTracker:
    def __init__(self, csv_file='expenses.csv'):
        self.csv_file = csv_file
        try:
            self.data = pd.read_csv(csv_file)
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])

    def load_data(self):  # Load existing data from CSV if available
        try:
            self.data = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])

    def add_expense(self, date, amount, category, description):
        if amount <= 0:
            print("\nError: Amount must be a positive number.")
            return
        new_expense = {'Date': date, 'Amount': amount, 'Category': category, 'Description': description}
        self.data = pd.concat([self.data, pd.DataFrame([new_expense])], ignore_index=True)
        print("\n✅ Expense added successfully!")

    def get_summary(self):
        total = self.data['Amount'].sum()
        avg = self.data['Amount'].mean()
        print(f" >> Total Spending: ₹{total:.2f}")
        print(f" >> Average Spending: ₹{avg:.2f}")

    def filter_expenses(self, condition):
        return self.data.query(condition)

    def generate_report(self):
        print("\n----> Expense Summary Report <----")
        self.get_summary()
        print("\n>> Category-wise Total Spending:")
        print(self.data.groupby('Category')['Amount'].sum())
        print("\n>> Monthly Spending Summary:")
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        print(self.data.groupby(self.data['Date'].dt.to_period('M'))['Amount'].sum())

    def save_data(self):
        self.data.to_csv(self.csv_file, index=False)
        print("💾 Data saved to CSV.")

    def bar_chart(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        plt.figure(figsize=(8, 5))
        sns.barplot(data=self.data, x='Category', y='Amount', estimator=sum)
        plt.title("Total Expenses by Category")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    def line_chart(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        monthly = self.data.groupby(self.data['Date'].dt.to_period('M'))['Amount'].sum()
        monthly.index = monthly.index.to_timestamp()
        plt.figure(figsize=(8, 5))
        plt.plot(monthly.index, monthly.values, marker='o')
        plt.title("Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Amount")
        plt.grid()
        plt.tight_layout()
        plt.show()

    def pie_chart(self):
        plt.figure(figsize=(6, 6))
        self.data.groupby('Category')['Amount'].sum().plot.pie(autopct='%1.1f%%')
        plt.title("Spending Distribution by Category")
        plt.tight_layout()
        plt.show()

    def histogram_chart(self):
        plt.figure(figsize=(8, 5))
        plt.hist(self.data['Amount'], bins=10, color='skyblue', edgecolor='black')
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    def visualize_data(self):
        if self.data.empty:
            print("❌ No data to visualize.")
            return

        print("\nChoose a visualization option:")
        print("1. 📊 Bar Chart (Total expenses by category)")
        print("2. 📈 Line Chart (Monthly spending trend)")
        print("3. 🥧 Pie Chart (Spending by category)")
        print("4. 📉 Histogram (Frequency of expense amounts)")
        print("5. 🔁 All Charts")

        vis_choice = input("\nEnter your choice: ")

        if vis_choice == '1':
            self.bar_chart()
        elif vis_choice == '2':
            self.line_chart()
        elif vis_choice == '3':
            self.pie_chart()
        elif vis_choice == '4':
            self.histogram_chart()
        elif vis_choice == '5':
            self.bar_chart()
            self.line_chart()
            self.pie_chart()
            self.histogram_chart()
        else:
            print("😵‍💫 Invalid choice for visualization.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.load_data()  # Load data from CSV at program start

    while True:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Smart Expense Tracker Menu")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1. ➕ Add Expense")
        print("2. 👁️ Show Summary")
        print("3. 📑 Filter Expenses")
        print("4. 📈 Generate Report")
        print("5. 📊 Visualize Data")
        print("6. 🗃️ Save and Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            date = input("\nEnter date (Format must be like YYYY-MM-DD): ")
            try:
                amount = float(input("      Enter amount: "))
            except ValueError:
                print("😵‍💫 Invalid amount please Try again 🙏🏻")
                continue
            category = input("      Enter category (e.g., Food, Transport): ")
            description = input("      Enter description: ")
            tracker.add_expense(date, amount, category, description)

        elif choice == '2':
            tracker.get_summary()

        elif choice == '3':
            print("\nSelect a category to filter:")
            print("1. 🍱 Food")
            print("2. 🚕 Transport")
            print("3. 🎭 Entertainment")
            print("4. 📋 Utilities")
            print("5. 🛍️ Shopping")

            user_choice = input("\n   Enter your choice: ")

            if user_choice == '1':
                category = '🍱 Food'
            elif user_choice == '2':
                category = '🚕 Transport'
            elif user_choice == '3':
                category = '🎭 Entertainment'
            elif user_choice == '4':
                category = '📋 Utilities'
            elif user_choice == '5':
                category = '🛍️ Shopping'
            else:
                print("😵‍💫 Invalid choice. 🙏🏻 Please try again.")
                category = None

            if category:
                condition = "Category == '{}'".format(category)
                result = tracker.filter_expenses(condition)
                if result.empty:
                    print("\n⚠️ No expenses found for this category.")
                else:
                    print("\n📋 Filtered Expenses:\n")
                    print(result)

            # if category:
            #     condition = "Category == '{}'".format(category)
            #     result = tracker.filter_expenses(condition)
            #     print(result)

        elif choice == '4':
            tracker.generate_report()

        elif choice == '5':
            tracker.visualize_data()

        elif choice == '6':
            tracker.save_data()
            print("🚫 Exiting... Goodbye!🙋🏻‍♀️")
            break
        else:
            print("😵‍💫 Invalid choice. 🙏🏻 Please enter a number between 1 to 6.")
