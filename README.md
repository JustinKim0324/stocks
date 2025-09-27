# Stock Infographics Repo

이 Repo는 6개 주요 기술주(테슬라, 엔비디아, 애플, 알파벳, 메타, 마이크로소프트)에 대한 상승/하락 요인 인포그래픽 HTML 파일을 저장하고, 매일 자동 업데이트하는 곳입니다. 각 파일은 주가 차트(TradingView 임베드), 성과 테이블, 최신 시황 기반 요인 목록을 포함해요.

## 대상 종목 리스트
- **Tesla (TSLA)**: tesla.html – EV/자율주행/에너지 중심.
- **Nvidia (NVDA)**: nvidia.html – AI 칩/반도체 리더.
- **Apple (AAPL)**: apple.html – 소비자 기기/서비스 생태계.
- **Alphabet (GOOG)**: alphabet.html – 검색/AI/클라우드.
- **Meta (META)**: meta.html – 소셜미디어/AI 광고.
- **Microsoft (MSFT)**: msft.html – 클라우드/AI 소프트웨어.

## 자동 업데이트 워크플로
- **매일 오전 9시 (UTC)**: GitHub Actions가 실행돼 각 HTML 파일 업데이트.
  - 주가/성과: yfinance API로 전일 마감 데이터 끌어옴.
  - 요인 내용: X 트렌드, 뉴스 API, 커뮤니티 검색으로 최신 시황 분석 후 재작성 (상승/하락 8개씩, 구체적 뉴스 반영).
  - 차트: TradingView 위젯 유지 (실시간).
- **호스팅**: GitHub Pages로 연결[](https://yourusername.github.io/stock-infographics/). 푸시될 때 자동 배포.
- **커스텀**: 새 종목 추가 시 종목 리스트 업데이트하고 Actions YAML 수정.

## 사용법
- 파일 다운로드: 각 .html 파일 브라우저에서 열기.
- 기여: 이슈나 PR로 피드백 주세요.
- 라이선스: MIT (자유 사용).

자세한 워크플로: [.github/workflows/daily-update.yml](.github/workflows/daily-update.yml) 확인.

(마지막 업데이트: 2025-09-27)
