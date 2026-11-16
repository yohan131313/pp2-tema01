class BudgetManager:
    def __init__(self, total_budget, fixed_manager):
        self.total_budget = total_budget
        self.fixed_manager = fixed_manager

        # 카테고리별 예산
        self.category_budgets = {}

        # 경고 관리자
        self.warning_manager = BudgetWarningManager()

    # 카테고리별 예산 설정
    def set_category_budget(self, category, amount):
        if amount < 0:
            raise ValueError("예산은 음수일 수 없습니다.")

        self.category_budgets[category] = amount

    # 전체 사용 가능 예산
    def get_available_budget(self):
        available = (
            self.total_budget
            - self.fixed_manager.get_total_expense()
        )

        if available < 0:
            raise ValueError("고정지출이 전체 예산을 초과했습니다.")

        return available

    # 전체 일반 소비 합계
    def get_total_used(self, expenses):
        return sum(e.amount for e in expenses)

    # 카테고리별 소비 합계
    def get_category_used(self, expenses, category):
        return sum(
            e.amount for e in expenses
            if e.category == category
        )

    # 전체 남은 예산
    def get_remaining_budget(self, expenses):
        return (
            self.get_available_budget()
            - self.get_total_used(expenses)
        )

    # 카테고리별 남은 예산
    def get_category_remaining(self, expenses, category):
        budget = self.category_budgets.get(category, 0)
        used = self.get_category_used(expenses, category)

        return budget - used

    # 전체 예산 사용률
    def get_total_usage_rate(self, expenses):
        available = self.get_available_budget()

        if available == 0:
            return 0

        return self.get_total_used(expenses) / available * 100

    # 카테고리별 예산 사용률
    def get_category_usage_rate(self, expenses, category):
        budget = self.category_budgets.get(category, 0)

        if budget == 0:
            return 0

        used = self.get_category_used(expenses, category)

        return used / budget * 100

    # 전체 예산 경고
    def get_total_warning(self, expenses):
        rate = self.get_total_usage_rate(expenses)
        return self.warning_manager.check_warning(rate)

    # 카테고리별 예산 경고
    def get_category_warning(self, expenses, category):
        rate = self.get_category_usage_rate(expenses, category)
        return self.warning_manager.check_warning(rate)

    # 카테고리별 예산 현황 출력
    def show_category_budget(self, expenses):
        print("\n===== 카테고리별 예산 현황 =====")

        for category, budget in self.category_budgets.items():
            used = self.get_category_used(expenses, category)
            remaining = budget - used
            rate = self.get_category_usage_rate(expenses, category)

            print(f"\n[{category}]")
            print(f"설정 예산: {budget:,}원")
            print(f"현재 소비: {used:,}원")
            print(f"남은 예산: {remaining:,}원")
            print(f"사용률: {rate:.2f}%")
            print(f"상태: {self.get_category_warning(expenses, category)}")

    # 전체 예산 현황 출력
    def show_total_budget(self, expenses):
        available = self.get_available_budget()
        used = self.get_total_used(expenses)
        remaining = available - used
        rate = self.get_total_usage_rate(expenses)

        print("\n===== 전체 예산 현황 =====")
        print(f"전체 예산: {self.total_budget:,}원")
        print(f"고정지출: {self.fixed_manager.get_total_expense():,}원")
        print(f"사용 가능 예산: {available:,}원")
        print(f"현재 소비: {used:,}원")
        print(f"남은 예산: {remaining:,}원")
        print(f"사용률: {rate:.2f}%")
        print(f"상태: {self.get_total_warning(expenses)}")