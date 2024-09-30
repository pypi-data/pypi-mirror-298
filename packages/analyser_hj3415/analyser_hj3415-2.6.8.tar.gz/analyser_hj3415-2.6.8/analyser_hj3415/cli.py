import argparse
import os

from utils_hj3415 import noti, utils
from utils_hj3415.helpers import SettingsManager
from analyser_hj3415.myredis import red_ranking, mil_n_score, red_n_score
from db_hj3415 import myredis


# 파일 경로 상수
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')


class AnalyserSettingsManager(SettingsManager):
    DEFAULT_SETTINGS = {
        'EXPECT_EARN': 0.06,
    }
    TITLES = DEFAULT_SETTINGS.keys()

    def set_value(self, title: str, value: str):
        assert title in self.TITLES, f"title 인자는 {self.TITLES} 중에 있어야 합니다."
        self.settings_dict[title] = value
        self.save_settings()
        print(f"{title}: {value}가 저장되었습니다")

    def get_value(self, title: str):
        assert title in self.TITLES, f"title 인자는 {self.TITLES} 중에 있어야 합니다."
        return self.settings_dict.get(title, self.DEFAULT_SETTINGS[title])

    def reset_value(self, title: str):
        assert title in self.TITLES, f"title 인자는 {self.TITLES} 중에 있어야 합니다."
        self.set_value(title, self.DEFAULT_SETTINGS[title])
        print(f"{title}이 기본값 ({self.DEFAULT_SETTINGS[title]}) 으로 초기화 되었습니다.")


def analyser_manager():
    settings_manager = AnalyserSettingsManager(SETTINGS_FILE)
    expect_earn_from_setting = settings_manager.get_value('EXPECT_EARN')

    parser = argparse.ArgumentParser(description="Analyser Commands")
    type_subparsers = parser.add_subparsers(dest='type', help='분석 타입')

    # red 명령어 서브파서
    red_parser = type_subparsers.add_parser('red', help='red 타입')
    red_subparser = red_parser.add_subparsers(dest='command', help='red 관련된 명령')
    # red - ranking 파서
    ranking_parser = red_subparser.add_parser('ranking', help='red 랭킹 책정 및 레디스 저장')
    ranking_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    ranking_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    ranking_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')
    # red - score 파서
    score_parser = red_subparser.add_parser('score', help='red score 책정 및 레디스 저장')
    score_parser.add_argument('code', type=str, help='종목코드 or all')
    score_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    score_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    score_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # mil 명령어 서브파서
    mil_parser = type_subparsers.add_parser('mil', help='millennial 타입')
    mil_subparser = mil_parser.add_subparsers(dest='command', help='mil 관련된 명령')
    # mil - score 파서
    score_parser = mil_subparser.add_parser('score', help='mil score 책정 및 레디스 저장')
    score_parser.add_argument('code', type=str, help='종목코드 or all')
    score_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    score_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    score_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # setting 명령어 서브파서
    setting_parser = type_subparsers.add_parser('setting', help='Set and Get settings')
    setting_subparser = setting_parser.add_subparsers(dest='command', help='setting 관련된 명령')
    # setting - set 파서
    set_parser = setting_subparser.add_parser('set', help='세팅값 저장')
    set_parser.add_argument('title', choices=AnalyserSettingsManager.TITLES, help='타이틀')
    set_parser.add_argument('value', help='세팅값')
    # setting - get 파서
    get_parser = setting_subparser.add_parser('get', help='타이틀 세팅값 불러오기')
    get_parser.add_argument('title', choices=AnalyserSettingsManager.TITLES, help='타이틀')
    # setting - print 파서
    setting_subparser.add_parser('print', help='전체 세팅값 출력')

    args = parser.parse_args()

    if args.type == 'red':
        if args.command == 'score':
            # 기대 수익률과 refresh 값 처리
            expect_earn = float(args.expect_earn if args.expect_earn is not None else expect_earn_from_setting)
            refresh = args.refresh if args.refresh else False

            # print(expect_earn, refresh)
            if args.code == 'all':
                print("**** red_n_score all code ****")
                for i, code in enumerate(myredis.Corps.list_all_codes()):
                    print(f'{i} / {code}')
                    red_n_score(code, expect_earn, refresh)
            else:
                assert utils.is_6digit(args.code), "code 인자는 6자리 숫자이어야 합니다."
                print(args.code, red_n_score(args.code, expect_earn, refresh))
            if args.noti:
                noti.telegram_to('manager', f"오늘의 red and score({args.code})를 레디스캐시에 저장했습니다.(유효 12시간)")

        elif args.command == 'ranking':
            # 기대 수익률과 refresh 값 처리
            expect_earn = float(args.expect_earn if args.expect_earn is not None else expect_earn_from_setting)
            refresh = args.refresh if args.refresh else False
            print(expect_earn, refresh)

            # red_ranking 함수 호출
            result = red_ranking(expect_earn, refresh)
            print(result)
            if args.noti:
                noti.telegram_to('manager', "오늘의 red ranking을 레디스캐시에 저장했습니다.(유효 12시간)")

    elif args.type == 'mil':
        if args.command == 'score':
            # 기대 수익률과 refresh 값 처리
            expect_earn = float(args.expect_earn if args.expect_earn is not None else expect_earn_from_setting)
            refresh = args.refresh if args.refresh else False

            if args.code == 'all':
                print("**** mil_n_score all code ****")
                for i, code in enumerate(myredis.Corps.list_all_codes()):
                    print(f'{i} / {code}')
                    mil_n_score(code, expect_earn, refresh)
            else:
                assert utils.is_6digit(args.code), "code 인자는 6자리 숫자이어야 합니다."
                print(args.code, mil_n_score(args.code, expect_earn, refresh))
            if args.noti:
                noti.telegram_to('manager', f"오늘의 mil and score({args.code})를 레디스캐시에 저장했습니다.(유효 12시간)")
    elif args.type == 'setting':
        if args.command == 'set':
            settings_manager.set_value(args.title, args.value)
        elif args.command == 'get':
            value = settings_manager.get_value(args.title)
            print(f"{args.title} 값: {value}")
        elif args.command == 'print':
            print(settings_manager.load_settings())
    else:
        parser.print_help()
