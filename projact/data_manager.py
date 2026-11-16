# 개인 소비 관리 가계부 - 데이터 처리 (F1~F3)
# 담당: 황현준

import csv
import os

# 데이터 파일 경로 (이 파이썬 파일과 같은 폴더의 data.txt)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.txt")

# 입력 가능한 내역 종류
TYPES = ("수입", "지출")


# 수입 및 지출 내역 1건을 담는 클래스
class Transaction:
    def __init__(self, date, record_type, category, amount, memo):
        self.date = date                # 날짜 (예: 2026-11-16)
        self.record_type = record_type  # 종류 ("수입" 또는 "지출")
        self.category = category        # 카테고리 (예: 식비, 용돈)
        self.amount = amount            # 금액 (정수)
        self.memo = memo                # 메모

    # 파일에 저장하기 쉽도록 내역을 리스트로 변환
    def to_list(self):
        return [self.date, self.record_type, self.category, self.amount, self.memo]


# 내역 전체를 관리하는 클래스
class DataManager:
    def __init__(self, data_file=DATA_FILE):
        self.records = []             # Transaction 객체들을 담는 리스트
        self.data_file = data_file    # 저장/불러오기에 사용할 파일 경로

    # 입력값 확인: 종류와 금액이 올바른지 검사
    def _is_valid(self, record_type, amount):
        # 종류가 "수입" 또는 "지출"이 아니면 오류
        if record_type not in TYPES:
            print("수입 또는 지출로 입력해주세요.")
            return False
        # 금액이 숫자가 아니거나 0 이하이면 오류(isdigit()은 음수나 문자가 섞이면 False를 반환)
        if not str(amount).isdigit() or int(amount) <= 0:
            print("금액은 0보다 큰 숫자로 입력해주세요.")
            return False
        return True

    # 인덱스 확인 : 해당 번호의 내역이 존재하는지 검사
    def _has(self, index):
        if 0 <= index < len(self.records):
            return True
        print("해당 내역이 없습니다.")
        return False

    # F1. 내역 추가
    def add_record(self, date, record_type, category, amount, memo):
        # 입력값이 잘못되었으면 추가하지 않고 종료
        if not self._is_valid(record_type, amount):
            return False
        # 금액은 정수로 변환해서 저장
        self.records.append(Transaction(date, record_type, category, int(amount), memo))
        print("내역이 추가되었습니다.")
        return True

    # F1. 내역 수정 (index번째 내역을 새 값으로 교체)
    def update_record(self, index, date, record_type, category, amount, memo):
        # 내역이 없거나 입력값이 잘못되었으면 수정하지 않고 종료
        if not self._has(index) or not self._is_valid(record_type, amount):
            return False
        self.records[index] = Transaction(date, record_type, category, int(amount), memo)
        print("내역이 수정되었습니다.")
        return True

    # F1. 내역 삭제
    def delete_record(self, index):
        if not self._has(index):
            return False
        del self.records[index]
        print("내역이 삭제되었습니다.")
        return True

    # 전체 내역 조회
    def get_records(self):
        return self.records

    # F2. 카테고리별 내역 조회 (카테고리가 같은 내역만 골라서 반환)
    def get_category_records(self, category):
        return [r for r in self.records if r.category == category]

    # F3. 데이터 저장 (내역을 한 줄씩 "|"로 구분해서 파일에 기록)
    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, delimiter="|").writerows(r.to_list() for r in self.records)
            print("데이터가 저장되었습니다.")
            return True
        except OSError as e:
            print("저장 오류:", e)
            return False

    # F3. 데이터 불러오기
    def load_data(self):
        try:
            with open(self.data_file, encoding="utf-8", newline="") as f:
                # 올바른 줄만 걸러냄: 항목 5개, 종류가 수입/지출, 금액이 0보다 큰 숫자
                rows = [r for r in csv.reader(f, delimiter="|")
                        if len(r) == 5 and r[1] in TYPES and r[3].isdigit() and int(r[3]) > 0]
            # 걸러낸 줄을 Transaction 객체로 바꿔 내역 목록을 교체
            self.records = [Transaction(d, t, c, int(a), m) for d, t, c, a, m in rows]
            print("데이터를 불러왔습니다.")
            return True
        except FileNotFoundError:
            print("저장된 데이터 파일이 없습니다.")
        except (OSError, csv.Error) as e:
            print("불러오기 오류:", e)
        return False


# 테스트 코드
if __name__ == "__main__":
    manager = DataManager("test_data.txt")  # 실제 데이터 파일과 분리해서 테스트

    # 내역 추가
    manager.add_record("2026-11-16", "지출", "식비", 10000, "점심 식사")
    manager.add_record("2026-11-16", "수입", "용돈", 50000, "부모님 용돈")

    # 전체 내역 출력
    print("\n[전체 내역]")
    for r in manager.get_records():
        print(r.date, r.record_type, r.category, r.amount, r.memo)

    # 저장 후 다시 불러오기
    manager.save_data()
    manager.load_data()
    print("\n저장된 내역 수:", len(manager.get_records()))