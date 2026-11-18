# 가계부 GUI - 기본틀 (customtkinter)
# 설치: pip install customtkinter
# 빈 창 + 상단 메뉴 + 화면 3개(내역/고정지출/예산)만 있는 뼈대.
# 위젯과 배치는 각 화면 클래스의 build()에 직접 추가하면 됨.

import customtkinter as ctk

# ----- 팀원 코드 연결 (import가 되는 걸 확인한 뒤 주석 해제) -----
# from data_manager import DataManager, TYPES
# from FixedExpenseManager import FixedExpenseManager
# from BudgetManager import BudgetManager


class BasePage(ctk.CTkFrame):
    """모든 화면의 공통 틀. TITLE만 바꿔서 화면마다 상속해서 사용"""
    TITLE = ""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app  # App 객체 (self.app.dm / fm / bm 으로 팀원 코드 접근)
        ctk.CTkLabel(self, text=self.TITLE,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=15, pady=15)
        self.build()

    def build(self):
        """위젯 만들고 배치하는 곳 (화면마다 덮어씀)"""
        pass

    def refresh(self):
        """화면 내용을 최신 데이터로 다시 그리는 곳 (화면마다 덮어씀)"""
        pass


class TransactionPage(BasePage):
    TITLE = "내역"

    def build(self):
        # TODO: 날짜/종류/카테고리/금액/메모 입력, 추가·삭제 버튼, 내역 표
        pass


class FixedExpensePage(BasePage):
    TITLE = "고정지출"

    def build(self):
        # TODO: 이름/카테고리/금액 입력, 추가·삭제 버튼, 목록 표, 합계 라벨
        pass


class BudgetPage(BasePage):
    TITLE = "예산"

    def build(self):
        # TODO: 전체 예산 입력, 현황 라벨, 사용률 진행바, 경고 문구
        pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("개인 소비 관리 가계부")
        self.geometry("1000x600")

        # ----- 팀원 코드 객체 (위 import 주석 해제 후 사용) -----
        # self.dm = DataManager()
        # self.fm = FixedExpenseManager()
        # self.bm = BudgetManager(0, self.fm)
        # self.dm.load_data()

        # ----- 상단 메뉴 -----
        nav = ctk.CTkFrame(self)
        nav.pack(fill="x")

        # ----- 화면들이 겹쳐 놓이는 영역 -----
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # 화면 만들기 + 메뉴 버튼 만들기
        self.pages = {}
        for page_class in (TransactionPage, FixedExpensePage, BudgetPage):
            name = page_class.TITLE
            page = page_class(container, self)
            page.grid(row=0, column=0, sticky="nsew")  # 전부 같은 자리에 겹쳐둠
            self.pages[name] = page
            ctk.CTkButton(nav, text=name,
                          command=lambda n=name: self.show_page(n)).pack(side="left", padx=5, pady=5)

        self.show_page("내역")

    def show_page(self, name):
        """name 화면을 맨 앞으로 가져옴 (다른 화면의 버튼에서도 self.app.show_page("예산") 가능)"""
        self.pages[name].refresh()
        self.pages[name].tkraise()

    def refresh_all(self):
        """데이터가 바뀌었을 때 모든 화면을 다시 그림"""
        for page in self.pages.values():
            page.refresh()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    App().mainloop()