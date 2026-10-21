import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

print("트랜스퍼마르크트 데이터 수집 시작...")

# 봇 차단을 방지하기 위해 일반 브라우저 헤더를 설정합니다.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 프리미어리그 메인 페이지 URL
url = "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1"

try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 프리미어리그 구단 목록 및 간단한 정보 수집
    teams_data = []
    table = soup.find('table', class_='items')
    
    if table:
        for row in table.select('tbody > tr'):
            name_tag = row.select_one('td.hauptlink.no-border-links a')
            value_tag = row.select_one('td.rechts.hauptlink')
            
            if name_tag and value_tag:
                teams_data.append({
                    'Team_Name': name_tag.text.strip(),
                    'Market_Value': value_tag.text.strip(),
                    'Updated_Date': datetime.date.today().strftime('%Y-%m-%d')
                })

    # 만약 파싱된 데이터가 없다면 기본 프레임 세팅
    if not teams_data:
        print("데이터 추출 실패 - 기본 프레임 생성")
        teams_data = [{'Team_Name': 'Premier League', 'Market_Value': 'N/A', 'Updated_Date': datetime.date.today().strftime('%Y-%m-%d')}]

    df = pd.DataFrame(teams_data)

    # data 폴더 생성 및 저장
    os.makedirs("data", exist_ok=True)
    file_path = "data/players_market_value.csv"
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"데이터 수집 완료! 저장 경로: {file_path}")

except Exception as e:
    print(f"데이터 수집 중 오류 발생: {e}")
    raise e
