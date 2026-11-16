class BudgetWarningManager:

    def check_warning(self, usage_rate):

        if usage_rate > 100:
            return "예산 초과! 지출을 줄여주세요."

        elif usage_rate >= 90:
            return "경고! 예산의 90% 이상 사용했습니다."

        elif usage_rate >= 75:
            return "경고! 예산의 75% 이상 사용했습니다."

        else:
            return "정상! 예산 범위 내입니다."