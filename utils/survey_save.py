import pandas as pd
import requests
from io import BytesIO
from collections import defaultdict
from typing import List
from schemas.survey_sch import SurveyQuestion, Choice
from utils.firebase_init import db


def download_excel_from_github(url: str) -> pd.DataFrame:
    """
    GitHub에서 엑셀 파일 다운로드 및 데이터프레임으로 변환.
    Args:
        url (str): 엑셀 파일의 GitHub Raw URL
    Returns:
        pd.DataFrame: 엑셀 데이터프레임
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        return df
    except Exception as e:
        raise ValueError(f"Failed to download or read Excel file: {e}")


def process_excel_data_grouped(df: pd.DataFrame) -> List[SurveyQuestion]:
    """
    엑셀 데이터를 문항별로 그룹화하고, 선택지를 배열로 변환.

    Args:
        df (pd.DataFrame): 엑셀 데이터프레임

    Returns:
        List[SurveyQuestion]: 문항 리스트
    """
    grouped_questions = defaultdict(list)

    # 데이터를 문항 번호로 그룹화
    for _, row in df.iterrows():
        grouped_questions[row["문항 번호"]].append(row)

    survey_questions = []

    # 각 그룹을 처리
    for num, rows in grouped_questions.items():
        base_row = rows[0]

        # 모든 행의 다른 데이터가 동일한지 확인
        for row in rows[1:]:
            if (
                row["문항 종류"] != base_row["문항 종류"] or
                row["문항 요인"] != base_row["문항 요인"] or
                row["문항 제목"] != base_row["문항 제목"]
            ):
                raise ValueError(f"Mismatch in data for question {num}")

        # 선택지를 번호 순서대로 정렬 후 배열로 변환
        rows_sorted = sorted(rows, key=lambda x: x["선택지 번호"])  # 선택지 번호로 정렬
        choices = [Choice(order=row["선택지 번호"], text=row["문항 선택지"]) for row in rows_sorted]

        # SurveyQuestion 모델 생성
        question = SurveyQuestion(
            num=base_row["문항 번호"],
            question_type=base_row["문항 종류"],
            factor=base_row["문항 요인"],
            title=base_row["문항 제목"],
            choices=choices,
            total_choices=len(choices)
        )
        survey_questions.append(question)

    return survey_questions


def save_grouped_survey_to_firestore(questions: List[SurveyQuestion]):
    """
    Firestore에 그룹화된 설문 데이터를 저장.

    Args:
        questions (List[SurveyQuestion]): 문항 리스트
    """
    try:
        # 'survey' 컬렉션에 각 문항 저장
        survey_ref = db.collection("survey")
        for question in questions:
            doc_ref = survey_ref.document()
            doc_ref.set(question.model_dump())  # Pydantic 모델을 dict로 변환하여 저장
        return {"message": "Survey saved successfully"}
    except Exception as e:
        raise ValueError(f"Failed to save survey to Firestore: {e}")


def load_and_save_survey_grouped(excel_url: str):
    """
    GitHub에서 엑셀 파일을 가져와 Firestore에 저장.

    Args:
        excel_url (str): GitHub에서 엑셀 파일 다운로드 URL
    """
    try:
        # 엑셀 파일 다운로드 및 데이터프레임 변환
        df = download_excel_from_github(excel_url)

        # 데이터 처리 및 Firestore 저장
        questions = process_excel_data_grouped(df)
        result = save_grouped_survey_to_firestore(questions)
        return result
    except Exception as e:
        return {"error": str(e)}
