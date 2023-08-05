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

def format_search_result(result):
    # 검색 결과 딕셔너리를 문자열로 변환하여 반환
    if not result:
        return "검색 결과가 없습니다."

    formatted_result = []
    for data in result:
        formatted_data = f"시/도: {data['1단계']}, 군/구: {data['2단계']}, 읍/면/동: {data['3단계']}, " \
                         f"격자 X: {data['격자 X']}, 격자 Y: {data['격자 Y']}"
        formatted_result.append(formatted_data)

    return "\n".join(formatted_result)
