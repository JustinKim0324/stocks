import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# 종목 리스트 (README에서 읽음, 여기서는 테슬라 예시)
stocks = {
    'tesla': {
        'symbol': 'TSLA',
        'html_file': 'tesla.html',
        'api_key': 'YOUR_NEWSAPI_KEY'  # NewsAPI.org에서 무료 키 발급 (선택, X 도구로 대체 가능)
    }
    # 다른 종목 추가: 'nvidia': {'symbol': 'NVDA', 'html_file': 'nvidia.html'}
}

def get_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")
    current_price = hist['Close'].iloc[-1]
    change = hist['Close'].iloc[-1] - hist['Open'].iloc[-1]
    change_pct = (change / hist['Open'].iloc[-1]) * 100
    return current_price, change_pct

def get_latest_news(symbol):
    # NewsAPI 예시 (키 필요, 또는 web_search 도구로 대체)
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={stocks['tesla']['api_key']}&sortBy=publishedAt&pageSize=10"
    response = requests.get(url)
    articles = response.json().get('articles', [])
    news_summary = [article['title'] + ': ' + article['description'][:100] for article in articles[:5]]
    return news_summary

def update_factors(news_summary):
    # Grok 스타일로 요인 생성 (간단 LLM 시뮬, 실제로는 API 호출)
    positive_factors = [
        "로보택시 이벤트 기대 랠리: 10월 데모 호평 예상, FSD 사용자 증가.",
        "에너지 부문 호조: 메가팩 Q3 매출 1.5배, 재생에너지 수요 폭증.",
        "애널리스트 PT 상향: Wedbush $600, 월간 주가 27% 상승 모멘텀.",
        "사이버트럭 생산 확대: 주간 1,000대, 옵티머스 로봇 공개 기대.",
        "IRA 세제 혜택: Q3 미국 판매 12% 증가, 2025 deliveries 180만 대 전망.",
        "Musk AI 전략: xAI 통합 FSD 강화, 투자자 신뢰 회복.",
        "NACS 네트워크: 충전소 4만 개 목표, 에너지 시너지.",
        "주주 환원: 자사주 매입 50억 달러, Q4 가이던스 긍정."
    ]
    negative_factors = [
        "유럽 판매 둔화: 20% 하락, 보조금 종료로 Q3 매출 감소.",
        "중국 경쟁: BYD 공세로 점유율 8% 하락, 브랜드 이미지 타격.",
        "가격 인하 마진 압박: Model Y 10% 인하, Q3 마진 18%로 하락.",
        "Musk 리스크: 정치 발언 논란, 트럼프 재선 보조금 폐지 우려.",
        "보조금 만료: 9/30 IRA 종료로 Q4 주문 둔화.",
        "밸류에이션 과열: PER 90배, 실적 미달 시 조정 위험.",
        "deliveries 우려: Q3 컨센서스 하회, 2025 성장률 9.4% 다운.",
        "EV 수요 둔화: 글로벌 5% 성장 둔화, 시장 점유율 18% 하락.",
        "금리 인상: 소비 둔화, EV 구매 지연 우려.",
        "FSD 규제: 사고 증가 NHTSA 조사, 로보택시 지연 가능성."
    ]
    return positive_factors, negative_factors

def update_html(file_path, price, change_pct, positive_factors, negative_factors):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # 주가 업데이트
    score_div = soup.find('div', class_='score')
    if score_div:
        score_div.string = f"테슬라 : {price:.2f} ({change_pct:+.2f}%)"
    
    # 성과 테이블 업데이트 (간단 예시, 실제로는 5일/30일/1년 계산)
    table = soup.find('table', class_='performance-table')
    if table:
        rows = table.find_all('tr')[1:]  # tbody rows
        rows[0].find_all('td')[1].string = '+6.8%'  # 최근 5일 예시
        rows[1].find_all('td')[1].string = '+18.5%'  # 30일
        rows[2].find_all('td')[1].string = '-12.3%'  # 1년
    
    # 상승 요인 업데이트
    up_section = soup.find('div', class_='section up')
    up_items = up_section.find_all('div', class_='item')
    for i, item in enumerate(up_items[:8]):
        strong = item.find('strong')
        if strong:
            strong.string = positive_factors[i][:strong.text.length]  # 요약
        p = item.find('p') or item
        p.string = positive_factors[i]
    
    # 하락 요인 업데이트 (유사)
    down_section = soup.find('div', class_='section down')
    down_items = down_section.find_all('div', class_='item')
    for i, item in enumerate(down_items[:10]):
        strong = item.find('strong')
        if strong:
            strong.string = negative_factors[i][:strong.text.length]
        p = item.find('p') or item
        p.string = negative_factors[i]
    
    # 날짜 업데이트
    estimated_div = soup.find('div', class_='estimated')
    if estimated_div:
        estimated_div.string = f"({datetime.now().strftime('%m월 %d일')} 기준, estimated by Justin Kim Research)"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

# 실행 예시 (테슬라 업데이트)
if __name__ == "__main__":
    stock = 'tesla'
    price, change_pct = get_stock_data(stocks[stock]['symbol'])
    news = get_latest_news(stock['symbol'])
    positive, negative = update_factors(news)
    update_html(stocks[stock]['html_file'], price, change_pct, positive, negative)
    print(f"테슬라 HTML 업데이트 완료: {price:.2f} ({change_pct:+.2f}%)")
