import pandas as pd

def filter_data(df, province=None, county=None, town=None):
    # 조건에 맞는 데이터 필터링
    filtered_data = df.copy()
    if province:
        filtered_data = filtered_data[filtered_data['1단계'] == province]

    if county:
        filtered_data = filtered_data[filtered_data['2단계'] == county]

    if town:
        filtered_data = filtered_data[filtered_data['3단계'] == town]

    # 검색 결과 딕셔너리 반환
    return filtered_data.to_dict(orient='records')

def server_filter_data(df, id):
    matching_rows = df[df['서버 ID'] == id]

    if matching_rows.empty:
        return None

    row_data = matching_rows.to_dict(orient='records')[0]
    result = {
        "서버 ID": str(row_data['서버 ID']),
        "1단계": str(row_data['1단계']),
        "2단계": str(row_data['2단계']),
        "3단계": str(row_data['3단계']),
        "Nx": int(row_data['Nx']),
        "Ny": int(row_data['Ny'])
    }

    return result