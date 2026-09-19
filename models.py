from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class Category(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    BILLS = "Bills"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    HEALTH = "Health"
    EDUCATION = "Education"
    SALARY = "Salary"
    OTHER = "Other"


CATEGORY_ICONS = {
    Category.FOOD: "🍔",
    Category.TRANSPORT: "🚗",
    Category.BILLS: "🧾",
    Category.ENTERTAINMENT: "🎬",
    Category.SHOPPING: "🛍️",
    Category.HEALTH: "🩺",
    Category.EDUCATION: "🎓",
    Category.SALARY: "💼",
    Category.OTHER: "📦",
}


# كلاس بيمثل عملية واحدة (دخل او مصروف)
@dataclass
class Transaction:
    id: int = None
    type: str = TransactionType.EXPENSE.value
    category: str = Category.OTHER.value
    amount: float = 0.0
    note: str = ""
    date: str = ""
    created_at: str = ""

    def __post_init__(self):
        # لو مفيش تاريخ متحدد، حط تاريخ النهاردة
        if not self.date:
            self.date = date.today().strftime("%Y-%m-%d")
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # المبلغ بيرجع سالب لو مصروف، موجب لو دخل (عشان حساب الرصيد يبقى سهل)
    def signed_amount(self):
        if self.type == TransactionType.INCOME.value:
            return self.amount
        return -self.amount

    def icon(self):
        try:
            return CATEGORY_ICONS[Category(self.category)]
        except ValueError:
            return "📦"