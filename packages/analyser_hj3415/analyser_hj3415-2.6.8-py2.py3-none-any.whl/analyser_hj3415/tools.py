import math
from typing import Tuple
from db_hj3415.myredis import C101, C103, C104

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def set_data(*args) -> list:
    """
    비유효한 내용 제거(None,nan)하고 중복된 항목 제거하고 리스트로 반환한다.
    여기서 set의 의미는 집합을 뜻함
    :param args:
    :return:
    """
    return [i for i in {*args} if i != "" and i is not math.nan and i is not None]


def calc당기순이익(code: str) -> Tuple[str, float]:
    """지배지분 당기순이익 계산

    일반적인 경우로는 직전 지배주주지분 당기순이익을 찾아서 반환한다.\n
    금융기관의 경우는 지배당기순이익이 없기 때문에\n
    계산을 통해서 간접적으로 구한다.\n
    """
    logger.debug(f'In the calc당기순이익... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        # print("*(지배)당기순이익: ", c103q.latest_value_pop2('*(지배)당기순이익'))
        return c103q.latest_value_pop2('*(지배)당기순이익')
    except:
        logger.warning(f"{code} - (지배)당기순이익이 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        c103q.page = 'c103손익계산서q'
        최근당기순이익date, 최근당기순이익value = c103q.sum_recent_4q('당기순이익')
        c103q.page = 'c103재무상태표q'
        비지배당기순이익date, 비지배당기순이익value = c103q.latest_value_pop2('*(비지배)당기순이익')

        # 가변리스트 언패킹으로 하나의 날짜만 사용하고 나머지는 버린다.
        date, *_ = set_data(최근당기순이익date, 비지배당기순이익date)
        계산된지배당기순이익value = 최근당기순이익value - 비지배당기순이익value

        return date, 계산된지배당기순이익value


def calc유동자산(code: str) -> Tuple[str, float]:
    """유효한 유동자산 계산

    일반적인 경우로 유동자산을 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc유동자산... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        return c103q.sum_recent_4q('유동자산')
    except:
        logger.warning(f"{code} - 유동자산이 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        d1, v1 = c103q.latest_value_pop2('현금및예치금')
        d2, v2 = c103q.latest_value_pop2('단기매매금융자산')
        d3, v3 = c103q.latest_value_pop2('매도가능금융자산')
        d4, v4 = c103q.latest_value_pop2('만기보유금융자산')
        logger.debug(f'현금및예치금 : {d1}, {v1}')
        logger.debug(f'단기매매금융자산 : {d2}, {v2}')
        logger.debug(f'매도가능금융자산 : {d3}, {v3}')
        logger.debug(f'만기보유금융자산 : {d4}, {v4}')

        date, *_ = set_data(d1, d2, d3, d4)
        계산된유동자산value = v1 + v2 + v3 + v4

        return date, 계산된유동자산value


def calc유동부채(code: str) -> Tuple[str, float]:
    """유효한 유동부채 계산

    일반적인 경우로 유동부채를 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc유동부채... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        return c103q.sum_recent_4q('유동부채')
    except:
        logger.warning(f"{code} - 유동부채가 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        d1, v1 = c103q.latest_value_pop2('당기손익인식(지정)금융부채')
        d2, v2 = c103q.latest_value_pop2('당기손익-공정가치측정금융부채')
        d3, v3 = c103q.latest_value_pop2('매도파생결합증권')
        d4, v4 = c103q.latest_value_pop2('단기매매금융부채')
        logger.debug(f'당기손익인식(지정)금융부채 : {d1}, {v1}')
        logger.debug(f'당기손익-공정가치측정금융부채 : {d2}, {v2}')
        logger.debug(f'매도파생결합증권 : {d3}, {v3}')
        logger.debug(f'단기매매금융부채 : {d4}, {v4}')

        date, *_ = set_data(d1, d2, d3, d4)
        계산된유동부채value = v1 + v2 + v3 + v4

        return date, 계산된유동부채value


def calc비유동부채(code: str) -> Tuple[str, float]:
    """유효한 비유동부채 계산

    일반적인 경우로 비유동부채를 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc비유동부채... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        return c103q.sum_recent_4q('비유동부채')
    except:
        logger.warning(f"{code} - 비유동부채가 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        # 보험관련업종은 예수부채가 없는대신 보험계약부채가 있다...
        d1, v1 = c103q.latest_value_pop2('예수부채')
        d2, v2 = c103q.latest_value_pop2('보험계약부채(책임준비금)')
        d3, v3 = c103q.latest_value_pop2('차입부채')
        d4, v4 = c103q.latest_value_pop2('기타부채')
        logger.debug(f'예수부채 : {d1}, {v1}')
        logger.debug(f'보험계약부채(책임준비금) : {d2}, {v2}')
        logger.debug(f'차입부채 : {d3}, {v3}')
        logger.debug(f'기타부채 : {d4}, {v4}')

        date, *_ = set_data(d1, d2, d3, d4)
        계산된비유동부채value = v1 + v2 + v3 + v4

        return date, 계산된비유동부채value


def calc유동비율(code: str, pop_count: int) -> Tuple[str, float]:
    """유동비율계산 - Blue에서 사용

    c104q에서 최근유동비율 찾아보고 유효하지 않거나 \n
    100이하인 경우에는수동으로 계산해서 다시 한번 평가해 본다.\n
    """
    logger.debug(f'In the calc유동비율... code:{code}')
    c104q = C104(code, 'c104q')
    유동비율date, 유동비율value = c104q.mymongo_c1034.latest_value('유동비율', pop_count=pop_count)
    logger.debug(f'{code} 유동비율 : {유동비율value}({유동비율date})')

    if math.isnan(유동비율value) or 유동비율value < 100:
        logger.warning('유동비율 is under 100 or nan..so we will recalculate..')
        유동자산date, 유동자산value = calc유동자산(code)
        유동부채date, 유동부채value = calc유동부채(code)

        c103q = C103(code, 'c103현금흐름표q')
        추정영업현금흐름date, 추정영업현금흐름value = c103q.sum_recent_4q('영업활동으로인한현금흐름')
        logger.debug(f'{code} 계산전 유동비율 : {유동비율value}({유동비율date})')

        계산된유동비율 = 0
        try:
            계산된유동비율 = round(((유동자산value + 추정영업현금흐름value) / 유동부채value) * 100, 2)
        except ZeroDivisionError:
            logger.debug(f'유동자산: {유동자산value} + 추정영업현금흐름: {추정영업현금흐름value} / 유동부채: {유동부채value}')
            계산된유동비율 = float('inf')
        finally:
            logger.debug(f'{code} 계산된 유동비율 : {계산된유동비율}')
            date, *_ = set_data(유동자산date, 유동부채date, 추정영업현금흐름date)
            return date, 계산된유동비율
    else:
        return 유동비율date, 유동비율value


def findFCF(code: str) -> dict:
    """
    FCF 계산
    Returns:
        dict: 계산된 fcf 딕셔너리 또는 영업현금흐름 없는 경우 - {}

    Note:
        CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.\n

    """
    c103y = C103(code, 'c103현금흐름표y')
    _, 영업활동현금흐름_dict = c103y.find_without_yoy('영업활동으로인한현금흐름')
    c103y.page = 'c103재무상태표y'
    _, capex = c103y.find_without_yoy('*CAPEX')

    logger.debug(f'영업활동현금흐름 {영업활동현금흐름_dict}')
    logger.debug(f'CAPEX {capex}')

    if len(영업활동현금흐름_dict) == 0:
        return {}

    if len(capex) == 0:
        # CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.
        logger.warning(f"{code} - CAPEX가 없는 업종으로 영업현금흐름을 그대로 사용합니다..")
        return 영업활동현금흐름_dict

    # 영업 활동으로 인한 현금 흐름에서 CAPEX 를 각 연도별로 빼주어 fcf 를 구하고 리턴값으로 fcf 딕셔너리를 반환한다.
    r_dict = {}
    for i in range(len(영업활동현금흐름_dict)):
        # 영업활동현금흐름에서 아이템을 하나씩 꺼내서 CAPEX 전체와 비교하여 같으면 차를 구해서 r_dict 에 추가한다.
        영업활동현금흐름date, 영업활동현금흐름value = 영업활동현금흐름_dict.popitem()
        # 해당 연도의 capex 가 없는 경우도 있어 일단 capex를 0으로 치고 먼저 추가한다.
        r_dict[영업활동현금흐름date] = 영업활동현금흐름value
        for CAPEXdate, CAPEXvalue in capex.items():
            if 영업활동현금흐름date == CAPEXdate:
                r_dict[영업활동현금흐름date] = round(영업활동현금흐름value - CAPEXvalue, 2)
    logger.debug(f'r_dict {r_dict}')
    # 연도순으로 정렬해서 딕셔너리로 반환한다.
    return dict(sorted(r_dict.items(), reverse=False))


def findPFCF(code: str) -> dict:
    """Price to Free Cash Flow Ratio(주가 대비 자유 현금 흐름 비율)계산

    PFCF = 시가총액 / FCF

    Note:
        https://www.investopedia.com/terms/p/pricetofreecashflow.asp
    """
    # marketcap 계산 (fcf가 억 단위라 시가총액을 억으로 나눠서 단위를 맞춰 준다)
    marketcap억 = get_marketcap(code) / 100000000
    if math.isnan(marketcap억):
        return {}

    # pfcf 계산
    fcf_dict = findFCF(code)
    logger.debug(f'fcf_dict : {fcf_dict}')
    pfcf_dict = {}
    for FCFdate, FCFvalue in fcf_dict.items():
        if FCFvalue == 0:
            pfcf_dict[FCFdate] = math.nan
        else:
            pfcf_dict[FCFdate] = round(marketcap억 / FCFvalue, 2)
    logger.debug(f'pfcf_dict : {pfcf_dict}')
    return pfcf_dict


def get_marketcap(code: str) -> float:
    """
    시가총액(원) 반환
    :param code:
    :return:
    """
    c101 = C101(code)
    try:
        return int(c101.get_recent()['시가총액'])
    except KeyError:
        return math.nan
