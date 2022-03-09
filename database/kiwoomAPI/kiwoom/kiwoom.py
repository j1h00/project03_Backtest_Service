import sys
import os
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errCode import *
from beautifultable import BeautifulTable
from PyQt5.QtTest import *
import sqlite3
from datetime import date


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        # 이벤트 루프 관련 변수
        self.login_event_loop = QEventLoop()
        self.account_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()

        # 계좌 관련 변수
        self.account_number = None
        self.total_buy_money = None
        self.total_evaluation_money = None
        self.total_evaluation_profit_and_loss_money = None
        self.total_yield = None
        self.account_stock_dict = {}
        self.not_signed_account_dict = {}

        # 예수금 관련 변수
        self.deposit = None
        self.withdraw_deposit = None
        self.order_deposit = None

        # 종목 분석 관련 변수
        # self.kosdaq_dict = {"삼성전자": "005930", "카카오": "035720", "네이버": "035420", "SK하이닉스": "000660", "현대차": "005380"}
        self.kosdaq_dict = {}
        self.kospi_dict = {}
        self.konex_dict = {}
        self.calculator_list = []

        # 종목 정보 가져오기 관련 변수
        self.portfolio_stock_dict = {}

        # 화면 번호
        self.screen_my_account = "1000"
        self.screen_calculation_stock = "2000"
        self.screen_real_stock = "3000"  # 종목별 할당할 화면 번호
        self.screen_order_stock = "4000"  # 종목별 할당할 주문용 화변 번호

        ########## 초기 작업 시작
        # self.create_kiwoom_instance()
        # self.event_collection()  # 이벤트와 슬롯을 메모리에 먼저 생성.
        # self.login()
        # input()

        # DB 연결
        self.conn = sqlite3.connect("../db/day_stock.db", isolation_level=None)
        # self.conn = sqlite3.connect("db/15min_stock.db", isolation_level=None)
        self.cursor = self.conn.cursor()

        # self.get_account_info()  # 계좌 번호만 얻어오기
        # self.get_deposit_info()  # 예수금 관련된 정보 얻어오기
        # self.get_account_evaluation_balance()  # 계좌평가잔고내역 얻어오기
        # self.not_signed_account()  # 미체결내역 얻어오기
        # self.get_stock_list_by_kospi(True)
        self.get_stock_list_by_kosdaq(True)  # False : DB 구축 x, True : DB 구축 o
        # self.get_stock_list_by_konex(False)  # False : DB 구축 x, True : DB 구축 o
        # self.get_hour_stock_list_by_kosdaq(False)  # False : DB 구축 x, True : DB 구축 o
        
        # self.merge_day_stock_kospi()
        self.merge_day_stock_kosdaq()

        # self.get_stock_kospi_financial_info()   # 코스피 주식기본정보요청     # 821개
        # self.get_stock_kosdaq_financial_info()   # 코스닥 주식기본정보요청    # 1552개
        # self.get_stock_konex_financial_info()   # 코넥스 주식기본정보요청       # 130개
        
        # self.update_day_stock_kospi() # 코스피 주식일봉차트 업데이트
        # self.update_day_stock_kosdaq() # 코스닥 주식일봉차트 업데이트
        # self.update_day_kiwoom_db() # DB 업데이트
        # self.granvile_theory()  # DB 구축 상태일 때만 유망한 종목을 뽑을 수 있음
        # self.read_file()  # 포트폴리오 읽어오기
        # self.screen_number_setting()  # 종목별 화면 번호 세팅
        ######### 초기 작업 종료
        self.menu()

    # COM 오브젝트 생성.
    def create_kiwoom_instance(self):
        # 레지스트리에 저장된 키움 openAPI 모듈 불러오기
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_collection(self):
        self.OnEventConnect.connect(self.login_slot)  # 로그인 관련 이벤트
        self.OnReceiveTrData.connect(self.tr_slot)  # 트랜잭션 요청 관련 이벤트

    def login(self):
        self.dynamicCall("CommConnect()")  # 시그널 함수 호출.
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        if err_code == 0:
            print("로그인에 성공하였습니다.")
        else:
            # os.system('cls')
            print("에러 내용 :", errors(err_code)[1])
            self.conn.close()
            sys.exit(0)
        self.login_event_loop.exit()

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        account_number = account_list.split(';')[0]
        self.account_number = account_number

    def menu(self):
        sel = ""
        while True:
            # os.system('cls')
            print("1. 현재 로그인 상태 확인")
            print("2. 사용자 정보 조회")
            print("3. 예수금 조회")
            print("4. 계좌 잔고 조회")
            print("5. 미체결 내역 조회")
            print("Q. 프로그램 종료")
            sel = input("=> ")

            if sel == "Q" or sel == "q":
                self.conn.close()
                sys.exit(0)

            if sel == "1":
                self.print_login_connect_state()
            elif sel == "2":
                self.print_my_info()
            elif sel == "3":
                self.print_get_deposit_info()
            elif sel == "4":
                self.print_get_account_evaulation_balance_info()
            elif sel == "5":
                self.print_not_signed_account()

    def print_login_connect_state(self):
        # os.system('cls')
        isLogin = self.dynamicCall("GetConnectState()")
        if isLogin == 1:
            print("\n현재 계정은 로그인 상태입니다.")
        else:
            print("\n현재 계정은 로그아웃 상태입니다.")
        input()

    def print_my_info(self):
        # os.system('cls')
        user_name = self.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        user_id = self.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        account_count = self.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT")

        print(f"\n이름 : {user_name}")
        print(f"ID : {user_id}")
        print(f"보유 계좌 수 : {account_count}")
        print(f"계좌번호 : {self.account_number}")
        input()

    def print_get_deposit_info(self):
        # os.system('cls')
        print(f"\n예수금 : {self.deposit}원")
        print(f"출금 가능 금액 : {self.withdraw_deposit}원")
        print(f"주문 가능 금액 : {self.order_deposit}원")
        input()

    def print_get_account_evaulation_balance_info(self):
        # os.system('cls')
        print("\n<싱글 데이터>")
        print(f"총 매입 금액 : {self.total_buy_money}원")
        print(f"총 평가 금액 : {self.total_evaluation_money}원")
        print(f"총 평가 손익 금액 : {self.total_evaluation_profit_and_loss_money}원")
        print(f"총 수익률 : {self.total_yield}%\n")

        table = self.make_table("계좌평가잔고내역요청")
        print("<멀티 데이터>")
        if len(self.account_stock_dict) == 0:
            print("보유한 종목이 없습니다!")
        else:
            print(f"보유 종목 수 : {len(self.account_stock_dict)}개")
            print(table)
        input()

    def make_table(self, sRQName):
        table = BeautifulTable()
        table = BeautifulTable(maxwidth=150)

        if sRQName == "계좌평가잔고내역요청":
            for stock_code in self.account_stock_dict:
                stock = self.account_stock_dict[stock_code]
                stockList = []
                for key in stock:
                    output = None

                    if key == "종목명":
                        output = stock[key]
                    elif key == "수익률(%)":
                        output = str(stock[key]) + "%"
                    elif key == "보유수량" or key == "매매가능수량":
                        output = str(stock[key]) + "개"
                    else:
                        output = str(stock[key]) + "원"
                    stockList.append(output)
                table.rows.append(stockList)
            table.columns.header = ["종목명", "평가손익", "수익률", "매입가", "보유수량", "매매가능수량", "현재가"]
            table.rows.sort('종목명')

        elif sRQName == "실시간미체결요청":
            for stock_order_number in self.not_signed_account_dict:
                stock = self.not_signed_account_dict[stock_order_number]
                stockList = [stock_order_number]
                for key in stock:
                    output = None
                    if key == "주문가격" or key == "현재가":
                        output = str(stock[key]) + "원"
                    elif '량' in key:
                        output = str(stock[key]) + "개"
                    elif key == "종목코드":
                        continue
                    else:
                        output = stock[key]
                    stockList.append(output)
                table.rows.append(stockList)
            table.columns.header = ["주문번호", "종목명", "주문구분", "주문가격", "주문수량", "미체결수량", "체결량", "현재가", "주문상태"]
            table.rows.sort('주문번호')
        return table

    def print_not_signed_account(self):
        # os.system('cls')
        print()
        table = self.make_table("실시간미체결요청")
        if len(self.not_signed_account_dict) == 0:
            print("미체결 내역이 없습니다!")
        else:
            print(table)
        input()

    def get_deposit_info(self, nPrevNext=0):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", " ")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "2")
        self.dynamicCall("CommRqData(QString, QString, int, QString)","예수금상세현황요청", "opw00001", nPrevNext, self.screen_my_account)

        self.account_event_loop.exec_()

    def get_account_evaluation_balance(self, nPrevNext=0):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", " ")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", nPrevNext, self.screen_my_account)

        if not self.account_event_loop.isRunning():
            self.account_event_loop.exec_()

    def not_signed_account(self, nPrevNext=0):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "전체종목구분", "0")
        self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "실시간미체결요청", "opt10075", nPrevNext, self.screen_my_account)

        if not self.account_event_loop.isRunning():
            self.account_event_loop.exec_()

    def tr_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "예수금")
            self.deposit = int(deposit)

            withdraw_deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "출금가능금액")
            self.withdraw_deposit = int(withdraw_deposit)

            order_deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "주문가능금액")
            self.order_deposit = int(order_deposit)
            self.cancel_screen_number(self.screen_my_account)
            self.account_event_loop.exit()

        elif sRQName == "계좌평가잔고내역요청":
            if (self.total_buy_money == None or self.total_evaluation_money == None
                    or self.total_evaluation_profit_and_loss_money == None or self.total_yield == None):
                total_buy_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총매입금액")
                self.total_buy_money = int(total_buy_money)

                total_evaluation_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가금액")
                self.total_evaluation_money = int(total_evaluation_money)

                total_evaluation_profit_and_loss_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가손익금액")
                self.total_evaluation_profit_and_loss_money = int(total_evaluation_profit_and_loss_money)

                total_yield = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총수익률(%)")
                self.total_yield = float(total_yield)

            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)

            for i in range(cnt):
                stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")
                stock_code = stock_code.strip()[1:]

                stock_name = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                stock_name = stock_name.strip()  # 필요 없는 공백 제거.

                stock_evaluation_profit_and_loss = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "평가손익")
                stock_evaluation_profit_and_loss = int(stock_evaluation_profit_and_loss)

                stock_yield = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "수익률(%)")
                stock_yield = float(stock_yield)

                stock_buy_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
                stock_buy_money = int(stock_buy_money)

                stock_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "보유수량")
                stock_quantity = int(stock_quantity)

                stock_trade_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매매가능수량")
                stock_trade_quantity = int(stock_trade_quantity)

                stock_present_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                stock_present_price = int(stock_present_price)

                if not stock_code in self.account_stock_dict:
                    self.account_stock_dict[stock_code] = {}

                self.account_stock_dict[stock_code].update({'종목명': stock_name})
                self.account_stock_dict[stock_code].update({'평가손익': stock_evaluation_profit_and_loss})
                self.account_stock_dict[stock_code].update({'수익률(%)': stock_yield})
                self.account_stock_dict[stock_code].update({'매입가': stock_buy_money})
                self.account_stock_dict[stock_code].update({'보유수량': stock_quantity})
                self.account_stock_dict[stock_code].update({'매매가능수량': stock_trade_quantity})
                self.account_stock_dict[stock_code].update({'현재가': stock_present_price})

            if sPrevNext == "2":
                self.get_account_evaluation_balance(2)
            else:
                self.cancel_screen_number(self.screen_my_account)
                self.account_event_loop.exit()

        elif sRQName == "실시간미체결요청":
            cnt = self.dynamicCall(
                "GetRepeatCnt(QString, QString)", sTrCode, sRQName)

            for i in range(cnt):
                stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목코드")
                stock_code = stock_code.strip()

                stock_order_number = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문번호")
                stock_order_number = int(stock_order_number)

                stock_name = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                stock_name = stock_name.strip()

                stock_order_type = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문구분")
                stock_order_type = stock_order_type.strip().lstrip('+').lstrip('-')

                stock_order_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문가격")
                stock_order_price = int(stock_order_price)

                stock_order_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문수량")
                stock_order_quantity = int(stock_order_quantity)

                stock_not_signed_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "미체결수량")
                stock_not_signed_quantity = int(stock_not_signed_quantity)

                stock_signed_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "체결량")
                stock_signed_quantity = int(stock_signed_quantity)

                stock_present_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                stock_present_price = int(stock_present_price.strip().lstrip('+').lstrip('-'))

                stock_order_status = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문상태")
                stock_order_status = stock_order_status.strip()

                if not stock_order_number in self.not_signed_account_dict:
                    self.not_signed_account_dict[stock_order_number] = {}

                self.not_signed_account_dict[stock_order_number].update({'종목코드': stock_code})
                self.not_signed_account_dict[stock_order_number].update({'종목명': stock_name})
                self.not_signed_account_dict[stock_order_number].update({'주문구분': stock_order_type})
                self.not_signed_account_dict[stock_order_number].update({'주문가격': stock_order_price})
                self.not_signed_account_dict[stock_order_number].update({'주문수량': stock_order_quantity})
                self.not_signed_account_dict[stock_order_number].update({'미체결수량': stock_not_signed_quantity})
                self.not_signed_account_dict[stock_order_number].update({'체결량': stock_signed_quantity})
                self.not_signed_account_dict[stock_order_number].update({'현재가': stock_present_price})
                self.not_signed_account_dict[stock_order_number].update({'주문상태': stock_order_status})

            if sPrevNext == "2":
                self.not_signed_account(2)
            else:
                self.cancel_screen_number(sScrNo)
                self.account_event_loop.exit()

        elif sRQName == "주식일봉차트조회요청":
            stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            #six_hundred_data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

            stock_code = stock_code.strip()
            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)  # 최대 600일

            for i in range(cnt):
                calculator_list = []

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                volume = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량")
                trade_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래대금")
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "일자")
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")

                calculator_list.append("")
                calculator_list.append(int(current_price))
                calculator_list.append(int(volume))
                calculator_list.append(int(trade_price))
                calculator_list.append(int(date))
                calculator_list.append(int(start_price))
                calculator_list.append(int(high_price))
                calculator_list.append(int(low_price))
                calculator_list.append("")

                self.calculator_list.append(calculator_list.copy())

            if sPrevNext == "2":
                self.day_kiwoom_db(stock_code, None, 2)
            else:
                self.save_day_kiwoom_db(stock_code)
                self.calculator_list.clear()
                self.calculator_event_loop.exit()

        elif sRQName == "주식일봉차트업데이트요청":
            stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            six_hundred_data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

            stock_code = stock_code.strip()
            self.calculator_list = six_hundred_data.copy()
            self.save_day_kiwoom_db(stock_code, True)
            self.calculator_list.clear()
            self.calculator_event_loop.exit()
        
        elif sRQName == "주식시봉차트조회요청":
            stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            #six_hundred_data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

            stock_code = stock_code.strip()
            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)  # 최대 600일

            for i in range(cnt):
                calculator_list = []

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                volume = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량")
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "체결시간")
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")

                calculator_list.append("")
                calculator_list.append(int(current_price))
                calculator_list.append(int(volume))
                calculator_list.append(int(date))
                calculator_list.append(int(start_price))
                calculator_list.append(int(high_price))
                calculator_list.append(int(low_price))
                calculator_list.append("")

                self.calculator_list.append(calculator_list.copy())

            if sPrevNext == "2":
                self.hour_kiwoom_db(stock_code, None, 2)
            else:
                self.save_hour_kiwoom_db(stock_code)
                self.calculator_list.clear()
                self.calculator_event_loop.exit()

        elif sRQName == "주식시봉차트업데이트요청":
            stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            six_hundred_data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

            stock_code = stock_code.strip()
            self.calculator_list = six_hundred_data.copy()
            self.save_hour_kiwoom_db(stock_code, True)
            self.calculator_list.clear()
            self.calculator_event_loop.exit()
        
        elif sRQName == "주식기본정보요청":
            stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            #six_hundred_data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

            stock_code = stock_code.strip()
            calculator_list = []
            종목코드 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            종목명 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목명")
            액면가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "액면가")
            자본금 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "자본금")
            상장주식 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "상장주식")
            신용비율 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "신용비율")
            연중최고 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "연중최고")
            연중최저= self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "연중최저")
            시가총액 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "시가총액")
            외인소진률 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "외인소진률")
            대용가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "대용가")
            PER = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "PER")
            EPS = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "EPS")
            ROE = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "ROE")
            PBR = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "PBR")
            EV = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "EV")
            BPS = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "BPS")
            매출액 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "매출액")
            영업이익 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "영업이익")
            당기순이익 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "당기순이익")
            최고250 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "250최고")
            최저250 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "250최저")
            시가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "시가")
            고가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "고가")
            저가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "저가")
            상한가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "상한가")
            하한가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "하한가")
            기준가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "기준가")
            예상체결가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "예상체결가")
            예상체결수량 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "예상체결수량")
            최고가일250 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "250최고가일")
            최고가대비율250 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "250최고가대비율")
            최저가일250 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "250최저가일")
            최저가대비율250 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "250최저가대비율")
            현재가 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "현재가")
            대비기호 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "대비기호")
            전일대비 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "전일대비")
            등락율 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "등락율")
            거래량 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "거래량")
            거래대비 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "거래대비")
            유통주식 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "유통주식")
            유통비율 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "유통비율")

            calculator_list.append("")
            calculator_list.append(종목코드.strip())
            calculator_list.append(종목명.strip())
            calculator_list.append(액면가.strip())
            calculator_list.append(자본금.strip())
            calculator_list.append(상장주식.strip())
            calculator_list.append(신용비율.strip())
            calculator_list.append(연중최고.strip())
            calculator_list.append(연중최저.strip())
            calculator_list.append(시가총액.strip())
            calculator_list.append(외인소진률.strip())
            calculator_list.append(대용가.strip())
            calculator_list.append(PER.strip())
            calculator_list.append(EPS.strip())
            calculator_list.append(PBR.strip())
            calculator_list.append(EV.strip())
            calculator_list.append(ROE.strip())
            calculator_list.append(BPS.strip())
            calculator_list.append(매출액.strip())
            calculator_list.append(영업이익.strip())
            calculator_list.append(당기순이익.strip())
            calculator_list.append(최고250.strip())
            calculator_list.append(최저250.strip())
            calculator_list.append(시가.strip())
            calculator_list.append(고가.strip())
            calculator_list.append(저가.strip())
            calculator_list.append(상한가.strip())
            calculator_list.append(하한가.strip())
            calculator_list.append(기준가.strip())
            calculator_list.append(예상체결가.strip())
            calculator_list.append(예상체결수량.strip())
            calculator_list.append(최고가일250.strip())
            calculator_list.append(최고가대비율250.strip())
            calculator_list.append(최저가일250.strip())
            calculator_list.append(최저가대비율250.strip())
            calculator_list.append(현재가.strip())
            calculator_list.append(대비기호.strip())
            calculator_list.append(전일대비.strip())
            calculator_list.append(등락율.strip())
            calculator_list.append(거래량.strip())
            calculator_list.append(거래대비.strip())
            calculator_list.append(유통주식.strip())
            calculator_list.append(유통비율.strip())
            calculator_list.append("")

            # print(calculator_list)
            self.calculator_list.append(calculator_list.copy())


            query = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(query)
            # table_name = "kospi_financial_info"
            # table_name = "kosdaq_financial_info"
            table_name = "konex_financial_info"

            # for row in self.cursor.fetchall():
            #     if row[0] == stock_name:
            #         return
            query = "CREATE TABLE IF NOT EXISTS {} \
                (종목코드 varchar, 종목명 varchar, 액면가 varchar, 자본금 varchar, 상장주식 varchar, 신용비율 varchar, \
                연중최고 varchar, 연중최저 varchar, 시가총액 varchar, 외인소진률 varchar, 대용가 varchar, PER VARCHAR, EPS varchar, \
                ROE varchar, PBR varchar, EV varchar, BPS varchar, 매출액 varchar, 영업이익 varchar, 당기순이익 varchar, 최고250 varchar, \
                최저250 varchar, 시가 varchar, 고가 varchar, 저가 varchar, 상한가 varchar, 하한가 varchar, 기준가 varchar, 예상체결가 varchar, \
                예상체결수량 varchar, 최고가일250 varchar, 최고가대비율250 varchar, 최저가일250 varchar, 최저가대비율250 varchar, \
                현재가 varchar, 대비기호 varchar, 전일대비 varchar, 등락율 varchar, 거래량 varchar, 거래대비 varchar, \
                유통주식 varchar, 유통비율 varchar)".format(table_name)
            self.cursor.execute(query)

            for item in self.calculator_list:
                calculator_tuple = tuple(item[1:-1])    # 41개
                query = "INSERT INTO {} (종목코드, 종목명, 액면가, 자본금, 상장주식, 신용비율, \
                연중최고, 연중최저, 시가총액, 외인소진률, 대용가, PER, EPS, \
                ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 최고250, \
                최저250, 시가, 고가, 저가, 상한가, 하한가, 기준가, 예상체결가, \
                예상체결수량, 최고가일250, 최고가대비율250, 최저가일250, 최저가대비율250, \
                현재가, 대비기호, 전일대비, 등락율, 거래량, 거래대비, 유통주식, 유통비율) \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name)
                self.cursor.execute(query, calculator_tuple)

            self.calculator_list.clear()
            self.calculator_event_loop.exit()
        

    def cancel_screen_number(self, sScrNo):
        self.dynamicCall("DisconnectRealData(QString)", sScrNo)

    def get_stock_list_by_kosdaq(self, isHaveDayData=False):
        # kosdaq_list = self.dynamicCall("GetCodeListByMarket(QString)", "10")
        # kosdaq_list = kosdaq_list.split(";")[:-1]

        # for stock_code in kosdaq_list:
        #     stock_name = self.dynamicCall("GetMasterCodeName(QString)", stock_code)
        #     if not stock_name in self.kosdaq_dict:
        #         self.kosdaq_dict[stock_name] = stock_code

        query = "SELECT * FROM kosdaq_basic_info"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.kosdaq_dict[row[0]] = row[1]    # row[0]: 회사명, row[1]: 종목코드


        if not isHaveDayData:
            for idx, stock_name in enumerate(self.kospi_dict):
                stock_code=self.kosdaq_dict[stock_name]
                print(idx, stock_name, stock_code)
                self.day_kiwoom_db(stock_code)
        

    def get_hour_stock_list_by_kosdaq(self, isHaveHourData=False):
        # kosdaq_list = self.dynamicCall("GetCodeListByMarket(QString)", "10")
        # kosdaq_list = kosdaq_list.split(";")[:-1]

        # for stock_code in kosdaq_list:
        #     stock_name = self.dynamicCall("GetMasterCodeName(QString)", stock_code)
        #     if not stock_name in self.kosdaq_dict:
        #         self.kosdaq_dict[stock_name] = stock_code

        if not isHaveHourData:
            # 모든 데이터
            # for idx, stock_name in enumerate(self.kosdaq_dict):
            #     self.dynamicCall("DisconnectRealData(QString)",
            #                      self.screen_calculation_stock)

            #     print(
            #         f"{idx + 1} / {len(self.kosdaq_dict)} : KOSDAQ Stock Code : {self.kosdaq_dict[stock_name]} is updating...")
            #     self.day_kiwoom_db(self.kosdaq_dict[stock_name])

            # 아래 주석 풀고 해당 데이터만 추가
            print("삼성전자")
            self.hour_kiwoom_db("005930")    # 삼성전자
            # print("카카오")
            # self.day_kiwoom_db("035720")    # 카카오
            # print("네이버")
            # self.day_kiwoom_db("035420")    # 네이버
            # print("SK하이닉스")
            # self.day_kiwoom_db("000660")    # SK하이닉스
            # self.day_kiwoom_db("005380")
            # print("현대차")

    def get_stock_list_by_kospi(self, isHaveDayData=False):
        query = "SELECT * FROM kospi_basic_info"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.kospi_dict[row[0]] = row[1]    # row[0]: 회사명, row[1]: 종목코드

        if not isHaveDayData:
            for idx, stock_name in enumerate(self.kospi_dict):
                stock_code=self.kospi_dict[stock_name]
                print(idx, stock_name, stock_code)
                self.day_kiwoom_db(stock_code)
        print("get stock list by kospi end")

    def get_stock_list_by_konex(self, isHaveDayData=False):
        query = "SELECT * FROM konex_basic_info"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.konex_dict[row[0]] = row[1]    # row[0]: 회사명, row[1]: 종목코드
        
        if not isHaveDayData:
            for idx, stock_name in enumerate(self.konex_dict):
                stock_code=self.konex_dict[stock_name]
                print(idx, stock_name, stock_code)
                self.day_kiwoom_db(stock_code)


    def get_stock_kospi_financial_info(self):
        for idx, stock_name in enumerate(self.kospi_dict):
            stock_code=self.kospi_dict[stock_name]
            print(idx, stock_name, stock_code)
            self.financial_kiwoom_db(stock_code)

    def get_stock_kosdaq_financial_info(self):
        for idx, stock_name in enumerate(self.kosdaq_dict):
            stock_code=self.kosdaq_dict[stock_name]
            print(idx, stock_name, stock_code)
            self.financial_kiwoom_db(stock_code)

    def get_stock_konex_financial_info(self):
        for idx, stock_name in enumerate(self.konex_dict):
            stock_code=self.konex_dict[stock_name]
            print(idx, stock_name, stock_code)
            self.financial_kiwoom_db(stock_code)

    def day_kiwoom_db(self, stock_code=None, date=None, nPrevNext=0, isUpdate=False):
        QTest.qWait(3600)  # 3.6초마다 딜레이

        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", stock_code)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", 1)

        if date != None:  # date가 None일 경우 date는 오늘 날짜 기준
            self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)

        if isUpdate:
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트업데이트요청", "opt10081", nPrevNext, self.screen_calculation_stock)
        else:
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트조회요청", "opt10081", nPrevNext, self.screen_calculation_stock)

        if not self.calculator_event_loop.isRunning():
            self.calculator_event_loop.exec_()

    def hour_kiwoom_db(self, stock_code=None, date=None, nPrevNext=0, isUpdate=False):
        QTest.qWait(3600)  # 3.6초마다 딜레이

        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", stock_code)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", 1)
        self.dynamicCall("SetInputValue(QString, QString)", "틱범위", 15)

        if isUpdate:
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식시봉차트업데이트요청", "opt10080", nPrevNext, self.screen_calculation_stock)
        else:
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식시봉차트조회요청", "opt10080", nPrevNext, self.screen_calculation_stock)

        if not self.calculator_event_loop.isRunning():
            self.calculator_event_loop.exec_()

    def financial_kiwoom_db(self, stock_code=None, date=None, nPrevNext=0):     # 3개월마다 갱신해줘야 함
        QTest.qWait(3600)  # 3.6초마다 딜레이
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", stock_code)
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", nPrevNext, self.screen_calculation_stock)

        if not self.calculator_event_loop.isRunning():
            self.calculator_event_loop.exec_()

    def save_day_kiwoom_db(self, stock_code=None, isUpdate=False):
        stock_name = self.dynamicCall("GetMasterCodeName(QString)", stock_code)
        table_name = "\"" + stock_code + "\""
        # table_name = "\"" + stock_name + "\""

        if isUpdate:
            for item in self.calculator_list:
                calculator_tuple = tuple(item[1:8])
                query = "SELECT * from {}".format(table_name)
                self.cursor.execute(query)

                is_date_in_db = False
                for row in self.cursor.fetchall():
                    if int(calculator_tuple[3]) == row[3]:
                        is_date_in_db = True
                        break

                if is_date_in_db:
                    return

                query = "INSERT INTO {} (current_price, volume, trade_price, date, \
                start_price, high_price, low_price) VALUES(?, ?, ?, ?, ?, ?, ?)".format(table_name)
                self.cursor.execute(query, calculator_tuple)
        else:
            query = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(query)

            for row in self.cursor.fetchall():
                if row[0] == stock_name:
                    return

            query = "CREATE TABLE IF NOT EXISTS {} \
                (current_price integer, volume integer, trade_price integer, \
                    date integer PRIMARY KEY, start_price integer, high_price integer, low_price integer)".format(table_name)
            self.cursor.execute(query)

            for item in self.calculator_list:
                calculator_tuple = tuple(item[1:-1])
                query = "INSERT INTO {} (current_price, volume, trade_price, date, \
                    start_price, high_price, low_price) VALUES(?, ?, ?, ?, ?, ?, ?)".format(table_name)
                self.cursor.execute(query, calculator_tuple)

    def update_day_stock_kospi(self):
        # 코스피 종목 중 db에 없는 종목은 새롭게 일봉 데이터를 추가. (오늘 날짜부터)
        for (idx, stock_name) in enumerate(self.kospi_dict):
            is_stock_name_in_db = False
            query = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                if self.kospi_dict[stock_name] == row[0]:
                    is_stock_name_in_db = True
                    break
            if not is_stock_name_in_db:
                print("add: ",end="")
                self.day_kiwoom_db(self.kospi_dict[stock_name])
                # return
            print(idx, self.kospi_dict[stock_name], stock_name)

        # # 튜플 내에서 가장 최근 날짜를 찾고, 오늘 날짜와 다르다면
        # # 오늘 날짜부터 (가장 최근 날짜 + 1)까지 새롭게 일봉 데이터를 추가.
        # today = int(date.today().isoformat().replace('-', ''))
        # query = "SELECT name FROM sqlite_master WHERE type='table'"
        # self.cursor.execute(query)
        # print(today, query)
        # for (idx, row) in enumerate(self.cursor.fetchall()):
        #     table_name = "\"" + self.kospi_dict[row[0]] + "\""
        #     query = "SELECT * from {}".format(table_name)
        #     self.cursor.execute(query)
        #     data_list = self.cursor.fetchall()
        #     if len(data_list) == 0:
        #         continue
        #     prev = data_list[len(data_list) - 1][3]

        #     if (prev < today):
        #         self.day_kiwoom_db(self.kosdaq_dict[row[0]], None, 0, True)
            
    def update_day_stock_kosdaq(self):
        # 코스닥 종목 중 db에 없는 종목은 새롭게 일봉 데이터를 추가. (오늘 날짜부터)
        for (idx, stock_name) in enumerate(self.kosdaq_dict):
            is_stock_name_in_db = False
            query = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                if stock_name == row[0]:
                    is_stock_name_in_db = True
                    break
            if not is_stock_name_in_db:
                print("add: ",end="")
                self.day_kiwoom_db(self.kosdaq_dict[stock_name])
                # return
            print(idx, self.kosdaq_dict[stock_name], stock_name)


    def update_day_kiwoom_db(self):
        # 코스닥 종목 중 db에 없는 종목은 새롭게 일봉 데이터를 추가. (오늘 날짜부터)
        for stock_name in self.kosdaq_dict:
            is_stock_name_in_db = False
            query = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                if stock_name == row[0]:
                    is_stock_name_in_db = True
                    break
            if not is_stock_name_in_db:
                self.day_kiwoom_db(self.kosdaq_dict[stock_name])
                # return
            print(self.kosdaq_dict[stock_name], stock_name)

        # 튜플 내에서 가장 최근 날짜를 찾고, 오늘 날짜와 다르다면
        # 오늘 날짜부터 (가장 최근 날짜 + 1)까지 새롭게 일봉 데이터를 추가.
        today = int(date.today().isoformat().replace('-', ''))
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        print(today, query)
        for (idx, row) in enumerate(self.cursor.fetchall()):
            table_name = "\"" + self.kosdaq_dict[row[0]] + "\""
            query = "SELECT * from {}".format(table_name)
            self.cursor.execute(query)
            data_list = self.cursor.fetchall()
            if len(data_list) == 0:
                continue
            prev = data_list[len(data_list) - 1][3]

            if (prev < today):
                print(
                    f"{idx + 1} / {len(self.kosdaq_dict)} : KOSDAQ Stock Code : {self.kosdaq_dict[row[0]]} is updating...")
                self.day_kiwoom_db(self.kosdaq_dict[row[0]], None, 0, True)
            else:
                print(
                    f"{idx + 1} / {len(self.kosdaq_dict)} : KOSDAQ Stock Code : {self.kosdaq_dict[row[0]]} is already updated!")

    def save_hour_kiwoom_db(self, stock_code=None, isUpdate=False, stock_name=None):
        # stock_name = self.dynamicCall("GetMasterCodeName(QString)", stock_code)
        table_name = "\"" + stock_code + "\""

        if isUpdate:
            for item in self.calculator_list:
                calculator_tuple = tuple(item[1:8])
                query = "SELECT * from {}".format(table_name)
                self.cursor.execute(query)

                is_date_in_db = False
                for row in self.cursor.fetchall():
                    if int(calculator_tuple[3]) == row[3]:
                        is_date_in_db = True
                        break

                if is_date_in_db:
                    return

                query = "INSERT INTO {} (current_price, volume, date, start_price, high_price, low_price) \
                VALUES(?, ?, ?, ?, ?, ?)".format(table_name)
                self.cursor.execute(query, calculator_tuple)
        else:
            query = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(query)

            for row in self.cursor.fetchall():
                if row[0] == stock_name:
                    return

            query = "CREATE TABLE IF NOT EXISTS {} \
                (current_price integer, volume integer, date integer PRIMARY KEY, start_price integer, high_price integer, low_price integer)".format(table_name)
            self.cursor.execute(query)

            for item in self.calculator_list:
                calculator_tuple = tuple(item[1:-1])
                query = "INSERT INTO {} (current_price, volume, date, start_price, high_price, low_price) \
                VALUES(?, ?, ?, ?, ?, ?)".format(table_name)
                self.cursor.execute(query, calculator_tuple)

    def update_hour_kiwoom_db(self):
        pass
    #     # 코스닥 종목 중 db에 없는 종목은 새롭게 일봉 데이터를 추가. (오늘 날짜부터)
    #     for stock_name in self.kosdaq_dict:
    #         is_stock_name_in_db = False
    #         query = "SELECT name FROM sqlite_master WHERE type='table'"
    #         self.cursor.execute(query)
    #         for row in self.cursor.fetchall():
    #             if stock_name == row[0]:
    #                 is_stock_name_in_db = True
    #                 break
    #         if not is_stock_name_in_db:
    #             self.day_kiwoom_db(self.kosdaq_dict[stock_name])
    #             # return
    #         print(self.kosdaq_dict[stock_name], stock_name)

    #     # 튜플 내에서 가장 최근 날짜를 찾고, 오늘 날짜와 다르다면
    #     # 오늘 날짜부터 (가장 최근 날짜 + 1)까지 새롭게 일봉 데이터를 추가.
    #     today = int(date.today().isoformat().replace('-', ''))
    #     query = "SELECT name FROM sqlite_master WHERE type='table'"
    #     self.cursor.execute(query)
    #     print(today, query)
    #     for (idx, row) in enumerate(self.cursor.fetchall()):
    #         table_name = "\"" + self.kosdaq_dict[row[0]] + "\""
    #         query = "SELECT * from {}".format(table_name)
    #         self.cursor.execute(query)
    #         data_list = self.cursor.fetchall()
    #         if len(data_list) == 0:
    #             continue
    #         prev = data_list[len(data_list) - 1][3]

    #         if (prev < today):
    #             print(
    #                 f"{idx + 1} / {len(self.kosdaq_dict)} : KOSDAQ Stock Code : {self.kosdaq_dict[row[0]]} is updating...")
    #             self.day_kiwoom_db(self.kosdaq_dict[row[0]], None, 0, True)
    #         else:
    #             print(
    #                 f"{idx + 1} / {len(self.kosdaq_dict)} : KOSDAQ Stock Code : {self.kosdaq_dict[row[0]]} is already updated!")

    def merge_day_stock_kospi(self):
        table_name="kospi_day_stock"
        for (idx, stock_name) in enumerate(self.kospi_dict):
            # is_stock_name_in_db = False
            stock_code=self.kospi_dict[stock_name]
            query = "SELECT * from [{}]".format(stock_code)
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                calculator_list=[stock_code]
                for item in row:
                    calculator_list.append(item)
                calculator_tuple = tuple(calculator_list)
                query = "INSERT INTO {} (code_number, current_price, volume, trade_price, date, start_price, high_price, low_price) \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(table_name)
                self.cursor.execute(query, calculator_tuple)
            print(idx, self.kospi_dict[stock_name], stock_name)

    def merge_day_stock_kosdaq(self):
        table_name="kosdaq_day_stock"
        for (idx, stock_name) in enumerate(self.kosdaq_dict):
            stock_code=self.kosdaq_dict[stock_name]
            query = "SELECT * from '{}'".format(stock_name)
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                calculator_list=[stock_code]
                for item in row:
                    calculator_list.append(item)
                calculator_tuple = tuple(calculator_list)
                query = "INSERT INTO {} (code_number, current_price, volume, trade_price, date, start_price, high_price, low_price) \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(table_name)
                self.cursor.execute(query, calculator_tuple)
                # break
            print(idx, self.kosdaq_dict[stock_name], stock_name)
            # break


    def granvile_theory(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            if (row[0][0] not in ['0', '1', '2', '3', '4']):    # 테이블 이름이 숫자로 시작해야함
                continue
            table_name = "\"" + row[0] + "\""
            query = "SELECT * from {}".format(table_name)
            self.cursor.execute(query)
            calculator_list = []
            for item in self.cursor.fetchall():
                itemList = list(item)
                itemList.insert(0, '')
                itemList.insert(len(itemList), '')
                calculator_list.append(itemList)
            calculator_list.reverse()
            # print(calculator_list)
            # if calculator_list == None or len(calculator_list) < 120:
            #     continue
            # for i in range(len(calculator_list)-119):
                # self.calculator(calculator_list[i:i+120], row[0])
            self.calculator(calculator_list, row[0])

    def calculator(self, calculator_list=None, stock_code=None):
        # pass_condition = False

        if calculator_list == None or len(calculator_list) < 140:
            return
        
        list_len=len(calculator_list)
        for cur in range(list_len-140):
            pass_condition = False
            # 120일 이동 평균선의 가격을 구함.
            total_price = 0
            for value in calculator_list[:120]:
                total_price += int(value[1])
            moving_average_price = total_price / 120

            # 오늘의 주가가 120일 이동 평균선에 걸쳐 있는가?
            is_stock_price_bottom = False
            today_price = None
            if int(calculator_list[cur][7]) <= moving_average_price and int(calculator_list[cur][6]) >= moving_average_price:
                is_stock_price_bottom = True
                today_price = int(calculator_list[0][6])
                # print("120일 안에 걸쳐있음")

            # 과거 20일 간의 일봉 데이터를 조회하면서 120일 이동 평균선보다 주가가 아래에 위치하는지 확인.
            prev_price = None
            if not is_stock_price_bottom:
                continue

            moving_average_price_prev = 0
            is_stock_price_prev_top = False
            # idx = cur+1

            # while True:
            for idx in range(cur+1, cur+20):
                # if len(calculator_list[idx:]) < 120:    # 120일 치가 있는지 계속 확인
                #     break

                total_price = 0
                for value in calculator_list[idx:idx+120]:
                    total_price += int(value[1])
                moving_average_price_prev = total_price / 120
                print(int(calculator_list[idx][6]), moving_average_price_prev, int(calculator_list[idx][7]))
                if moving_average_price_prev <= int(calculator_list[idx][6]):
                    break

                elif int(calculator_list[idx][7]) > moving_average_price_prev:
                    is_stock_price_prev_top = True
                    prev_price = int(calculator_list[idx][7])
                    break
                # idx += 1

            if is_stock_price_prev_top:
                if moving_average_price > moving_average_price_prev and today_price > prev_price:
                    pass_condition = True

            if not pass_condition:
                continue

            print("팝시다")
        
        # if pass_condition:
            # print("pass condition")
            # stock_name = self.dynamicCall("GetMasterCodeName(QString", stock_code)
            # f = open("files/condition_stock.txt", "a", encoding="UTF8")
            # f.write(
            #     f"{stock_code}\t{stock_name}\t{str(calculator_list[0][1])}\n")
            # f.close()

    def read_file(self):
        if os.path.exists("files/condition_stock.txt"):
            f = open("files/condition_stock.txt", "r", encoding="UTF8")

            lines = f.readlines()
            for line in lines:
                if line != "":
                    data = line.split("\t")

                    stock_code = data[0]
                    stock_name = data[1]
                    stock_price = int(data[2].split("\n")[0])
                    stock_price = abs(stock_price)

                    self.portfolio_stock_dict.update(
                        {stock_code: {"종목명": stock_name, "현재가": stock_price}})
            f.close()

    def screen_number_setting(self):
        screen_overwrite = []

        for stock_code in self.account_stock_dict:
            if stock_code not in screen_overwrite:
                screen_overwrite.append(stock_code)

        for order_number in self.not_signed_account_dict:
            stcoK_code = self.not_signed_account_dict[order_number]['종목코드']

            if stock_code not in screen_overwrite:
                screen_overwrite.append(stock_code)

        for stock_code in self.portfolio_stock_dict:
            if stock_code not in screen_overwrite:
                screen_overwrite.append(stock_code)

        # 화면 번호 할당.
        cnt = 1
        for stock_code in screen_overwrite:
            real_stock_screen = int(self.screen_real_stock)
            order_stock_screen = int(self.screen_order_stock)

            if (cnt % 50) == 0:
                real_stock_screen += 1
                self.screen_real_stock = str(real_stock_screen)

            if (cnt % 50) == 0:
                order_stock_screen += 1
                self.screen_order_stock = str(order_stock_screen)

            if stock_code in self.portfolio_stock_dict:
                self.portfolio_stock_dict[stock_code].update(
                    {"화면번호": str(self.screen_real_stock)})
                self.portfolio_stock_dict[stock_code].update(
                    {"주문용화면번호": str(self.screen_order_stock)})
            else:
                self.portfolio_stock_dict.update({stock_code: {"화면번호": str(
                    self.screen_real_stock), "주문용화면번호": str(self.screen_order_stock)}})

            cnt += 1
        print(self.portfolio_stock_dict)