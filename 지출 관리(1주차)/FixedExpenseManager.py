class FixedExpenseManager:
    def __init__(self):
        self.fixed_expenses = []

    # 고정지출 추가
    def add_expense(self, name, category, amount):
        if amount < 0:
            raise ValueError("금액은 음수일 수 없습니다.")

        expense = FixedExpense(name, category, amount)
        self.fixed_expenses.append(expense)

    # 고정지출 삭제
    def remove_expense(self, name):
        for expense in self.fixed_expenses:
            if expense.name == name:
                self.fixed_expenses.remove(expense)
                return True
        return False

    # 고정지출 수정
    def update_expense(self, name, new_amount):
        if new_amount < 0:
            raise ValueError("금액은 음수일 수 없습니다.")

        for expense in self.fixed_expenses:
            if expense.name == name:
                expense.amount = new_amount
                return True
        return False

    # 고정지출 목록 조회
    def show_expenses(self):
        for expense in self.fixed_expenses:
            print(expense)

    # 고정지출 총합 계산
    def get_total_expense(self):
        return sum(
            expense.amount
            for expense in self.fixed_expenses
        )