import os
import soccerdata as sd
import pandas as pd
import datetime

print("트랜스퍼마르크트 데이터 수집 시작...")

try:
    # 프리미어리그 선수 시장 가치 데이터 가져오기
    tm = sd.Transfermarkt(leagues='ENG-Premier League', seasons=2025)
    df = tm.read_player_market_values()

    # 인덱스 정리
    df = df.reset_index()

    # data 폴더가 없으면 자동 생성
    os.makedirs("data", exist_ok=True)

    # CSV 파일로 저장
    file_path = "data/players_market_value.csv"
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"데이터 수집 및 저장 완료: {file_path}")

except Exception as e:
    print(f"데이터 수집 중 오류 발생: {e}")
    exit(1)
