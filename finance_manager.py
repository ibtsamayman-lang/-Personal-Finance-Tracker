from datetime import datetime
import pandas as pd

from models import TransactionType, Category


class FinanceManager:
    def __init__(self, db):
        self.db = db
    def add_transaction(self, type_, category, amount, note, date_str):
        from models import Transaction
        t = Transaction(type=type_, category=category, amount=amount, note=note, date=date_str)
        t.id = self.db.add_transaction(t)
        return t
    def delete_transaction(self, transaction_id):
        self.db.delete_transaction(transaction_id)
    def get_all(self):
        return self.db.get_all_transactions()
    def get_balance(self):
        total = 0
        for t in self.get_all():
            total += t.signed_amount()
        return total
    def get_total_income(self):
        total = 0
        for t in self.get_all():
            if t.type == TransactionType.INCOME.value:
                total += t.amount
        return total
    def get_total_expenses(self):
        total = 0
        for t in self.get_all():
            if t.type == TransactionType.EXPENSE.value:
                total += t.amount
        return total
    def get_current_month_expenses_by_category(self):
        current_month = datetime.today().strftime("%Y-%m")
        totals = {}
        for t in self.get_all():
            if t.type == TransactionType.EXPENSE.value and t.date.startswith(current_month):
                if t.category not in totals:
                    totals[t.category] = 0
                totals[t.category] += t.amount
        return totals
    def get_budget_status(self):
        budgets = self.db.get_budgets()
        spent = self.get_current_month_expenses_by_category()
        status_list = []
        for category, limit in budgets.items():
            used = spent.get(category, 0)
            if limit > 0:
                percent = used / limit * 100
            else:
                percent = 0
            status_list.append({
                "category": category,
                "limit": limit,
                "spent": used,
                "remaining": limit - used,
                "percent": percent,
                "exceeded": used > limit,
            })
        return status_list
    def to_dataframe(self):
        transactions = self.get_all()
        if len(transactions) == 0:
            return pd.DataFrame(columns=["id", "type", "category", "amount", "note", "date"])
        rows = []
        for t in transactions:
            rows.append({"id": t.id, "type": t.type, "category": t.category,
                         "amount": t.amount, "note": t.note, "date": t.date})
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        return df
    def monthly_trend(self):
        df = self.to_dataframe()
        if df.empty:
            return df
        df["month"] = df["date"].dt.to_period("M").astype(str)
        signed_values = []
        for i, row in df.iterrows():
            if row["type"] == TransactionType.INCOME.value:
                signed_values.append(row["amount"])
            else:
                signed_values.append(-row["amount"])
        df["signed"] = signed_values
        result = df.groupby("month")["signed"].sum().reset_index()
        result["month"] = result["month"].astype(str)
        return result
    def get_savings_rate(self):
        income = self.get_total_income()
        expenses = self.get_total_expenses()
        if income == 0:
            return 0
        savings = income - expenses
        rate = savings / income * 100
        return rate
    def get_month_comparison(self):
        from datetime import datetime, timedelta
        today = datetime.today()
        current_month = today.strftime("%Y-%m")
        first_day_this_month = today.replace(day=1)
        last_day_previous_month = first_day_this_month - timedelta(days=1)
        previous_month = last_day_previous_month.strftime("%Y-%m")
        current_totals = {}
        previous_totals = {}
        for t in self.get_all():
            if t.type != TransactionType.EXPENSE.value:
                continue
            if t.date.startswith(current_month):
                if t.category not in current_totals:
                    current_totals[t.category] = 0
                current_totals[t.category] += t.amount
            elif t.date.startswith(previous_month):
                if t.category not in previous_totals:
                    previous_totals[t.category] = 0
                previous_totals[t.category] += t.amount

        all_categories = set(list(current_totals.keys()) + list(previous_totals.keys()))

        comparison = []
        for category in all_categories:
            current_amount = current_totals.get(category, 0)
            previous_amount = previous_totals.get(category, 0)
            if previous_amount > 0:
                change_percent = (current_amount - previous_amount) / previous_amount * 100
            else:
                change_percent = 0
            comparison.append({
                "category": category,
                "current": current_amount,
                "previous": previous_amount,
                "change_percent": change_percent,
            })

        return comparison
    
    def last_transaction_info(self):
        transactions = self.get_all()
        if not transactions:
            return None
        last_transaction = transactions[0]
        return {
            "date": last_transaction.date,
            "created_at": last_transaction.created_at,
        }