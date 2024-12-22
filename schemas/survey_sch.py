from pydantic import BaseModel
from typing import List

class Choice(BaseModel):
    order: int  # 선택지의 순서
    text: str  # 선택지의 내용

class SurveyQuestion(BaseModel):
    num: int  # 문항 번호
    question_type: str  # 문항 종류
    factor: str  # 문항 요인
    title: str  # 문항 제목
    choices: List[Choice]  # 선택지 목록
    total_choices: int  # 선택지 개수
