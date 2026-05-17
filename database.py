import os
import requests
import urllib.parse
import re
from datetime import datetime
import pytz
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

# .env 파일 로드 (로컬 개발 환경)
load_dotenv()

# 한국 표준시(KST) 타임존 설정
KST = pytz.timezone('Asia/Seoul')

def get_kst_now():
    """현재 시각을 KST로 반환 (timezone-naive)"""
    return datetime.now(KST).replace(tzinfo=None)

@st.cache_resource
def get_supabase_config():
    """Supabase 접속 정보 반환 (환경 변수 우선 방식)"""
    import os
    
    # 1. 먼저 구글 클라우드 환경 변수(os.environ)에서 가져오기
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    # 2. 환경 변수가 없다면 st.secrets (로컬 개발용) 확인
    if not url or not key:
        try:
            # .get() 메서드를 사용하여 키가 없어도 에러가 발생하지 않도록 함
            if "supabase" in st.secrets:
                url = url or st.secrets["supabase"].get("url")
                key = key or st.secrets["supabase"].get("key")
        except Exception:
            pass
            
    if not url or not key:
        # 더 이상 st.secrets 파일 경로 에러가 아닌, 값이 없다는 구체적 에러 메시지 출력
        raise Exception("환경 변수(SUPABASE_URL, SUPABASE_KEY)가 설정되지 않았습니다.")
        
    base_url = url.rstrip('/') + "/rest/v1"
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    return base_url, headers

class ConvWrapper:
    """기존 dot notation 호환 및 신규 통계 컬럼 지원 확장 래퍼 클래스"""
    def __init__(self, data):
        self.__dict__.update(data)
        # 기본값 설정 (KeyError 방지)
        self.curriculum_code = data.get("curriculum_code", "N/A")
        self.success = data.get("success", "N/A")
        self.total_turns = data.get("total_turns", 0)
        self.content_element = data.get("content_element", "N/A")
        
        if 'created_at' in data:
            try:
                ts = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                self.timestamp = ts.astimezone(KST).replace(tzinfo=None)
            except:
                self.timestamp = datetime.now()
        else:
            self.timestamp = datetime.now()

def parse_hidden_result_tag(answer_text):
    """
    AI 튜터의 응답 텍스트에서 [RESULT: ...] 숨겨진 태그를 파싱합니다.
    형식: [RESULT: {성취기준 코드} | {내용 요소} | {SUCCESS: Y/N} | {총 대화 Turn 수}]
    """
    # SUCCESS: Y 또는 그냥 Y 둘 다 견고하게 매칭하는 정규표현식(Regex)
    pattern = r'\[RESULT:\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(?:SUCCESS:\s*)?([YNyn])\s*\|\s*(\d+)\s*\]'
    match = re.search(pattern, answer_text)
    
    if match:
        return {
            "curriculum_code": match.group(1).strip(),
            "content_element": match.group(2).strip(),
            "success": match.group(3).strip().upper(),  # 'Y' 또는 'N'으로 정규화
            "total_turns": int(match.group(4).strip())
        }
    return None

def save_conversation_to_db(student_id: str, device_id: str, question: str, answer: str, 
                            content_element: str = None):
    """대화 데이터를 데이터베이스에 저장 (AI 히든 태그 자동 분석 기능 포함)"""
    base_url, headers = get_supabase_config()
    
    # 기본 데이터 구조 정의
    data = {
        "student_id": student_id,
        "device_id": device_id,
        "question": question,
        "answer": answer,
        "content_element": content_element,
        "curriculum_code": "N/A",  # 기본값
        "success": "N/A",          # 기본값
        "total_turns": 0           # 기본값
    }
    
    # AI 응답 내 마스터 태그 검사 및 데이터 고도화 (바이브 엔지니어링의 핵심)
    parsed_meta = parse_hidden_result_tag(answer)
    if parsed_meta:
        data["curriculum_code"] = parsed_meta["curriculum_code"]
        data["content_element"] = parsed_meta["content_element"]
        data["success"] = parsed_meta["success"]
        data["total_turns"] = parsed_meta["total_turns"]
    
    post_headers = headers.copy()
    post_headers["Prefer"] = "return=representation"
    
    resp = requests.post(f"{base_url}/conversations", headers=post_headers, json=data)
    if resp.status_code in (200, 201):
        res_data = resp.json()
        return res_data[0]["id"] if res_data else None
    else:
        error_msg = f"Supabase Insert Error: {resp.text}"
        st.error(error_msg)
        raise Exception(error_msg)

def get_all_conversations():
    """모든 대화 데이터 조회"""
    base_url, headers = get_supabase_config()
    resp = requests.get(f"{base_url}/conversations?select=*&order=created_at.desc", headers=headers)
    if resp.status_code == 200:
        return [ConvWrapper(d) for d in resp.json()]
    return []

def get_conversations_by_student(student_id: str):
    """특정 학생의 대화 데이터 조회"""
    base_url, headers = get_supabase_config()
    s_id = urllib.parse.quote(student_id)
    resp = requests.get(f"{base_url}/conversations?select=*&student_id=eq.{s_id}&order=created_at.desc", headers=headers)
    if resp.status_code == 200:
        return [ConvWrapper(d) for d in resp.json()]
    return []

# --- 🚀 [논문 4장 하이패스용] 고급 분석 통계 함수군 ---

def get_statistics():
    """전체 연구 통계 조회 (성공률 및 평균 턴 수 지표 확장)"""
    base_url, headers = get_supabase_config()
    
    # 1. 총 대화 로그 수 산출
    cnt_headers = headers.copy()
    cnt_headers["Prefer"] = "count=exact"
    resp = requests.get(f"{base_url}/conversations?select=id", headers=cnt_headers)
    total_conversations = 0
    if resp.status_code in (200, 206):
        crange = resp.headers.get("Content-Range", "")
        if crange and "/" in crange:
            try:
                total_conversations = int(crange.split("/")[-1])
            except ValueError:
                total_conversations = len(resp.json())
        else:
            total_conversations = len(resp.json())
            
    # 2. 고유 학생 수 및 고급 메타데이터 통계 분석 (Pandas 연산)
    resp2 = requests.get(f"{base_url}/conversations?select=student_id,success,total_turns", headers=headers)
    total_students = 0
    success_rate = 0.0
    avg_total_turns = 0.0
    
    if resp2.status_code == 200:
        data = resp2.json()
        if data:
            df = pd.DataFrame(data)
            total_students = df['student_id'].nunique()
            
            # 한 문항 완결 데이터 필터링 (N/A 제외)
            df_completed = df[df['success'].isin(['Y', 'N'])]
            
            if not df_completed.empty:
                # 스스로 추론 성공률 계산 (SUCCESS: Y 비율)
                success_count = len(df_completed[df_completed['success'] == 'Y'])
                success_rate = round((success_count / len(df_completed)) * 100, 1)
                
                # 대화 완결까지 걸린 평균 턴(Turn) 수 계산
                avg_total_turns = round(df_completed['total_turns'].mean(), 1)
            
    return {
        'total_conversations': total_conversations,
        'total_students': total_students,
        'avg_per_student': round(total_conversations / total_students, 1) if total_students > 0 else 0,
        'success_rate_percent': success_rate,        # 4장 교실 전체 성공률 지표로 활용
        'avg_turns_to_complete': avg_total_turns     # 4장 학습 효율성 지표로 활용
    }

def get_content_element_detailed_analysis():
    """
    [논문 통계 방어 치트키] 분자 내용 요소별 스스로 추론 성공률 및 평균 대화 깊이 분석
    출력 형식: DataFrame 변환용 딕셔너리 리스트
    """
    base_url, headers = get_supabase_config()
    resp = requests.get(f"{base_url}/conversations?select=content_element,success,total_turns", headers=headers)
    
    if resp.status_code != 200:
        return []
        
    data = resp.json()
    if not data:
        return []
        
    df = pd.DataFrame(data)
    # 데이터 전처리
    df = df.dropna(subset=['content_element', 'success'])
    df = df[df['success'].isin(['Y', 'N'])]
    
    if df.empty:
        return []
        
    analysis_results = []
    # 각 분자/내용 요소별로 그룹화 정밀 분석
    for element, group in df.groupby('content_element'):
        total_cases = len(group)
        success_cases = len(group[group['success'] == 'Y'])
        success_rate = round((success_cases / total_cases) * 100, 1)
        avg_turns = round(group['total_turns'].mean(), 1)
        
        analysis_results.append({
            "content_element": element,      # 예: CO2의 구조 추론
            "total_attempts": total_cases,    # 누적 시도 횟수
            "success_rate": success_rate,    # 자력 추론 성공률 (%)
            "avg_dialogue_turns": avg_turns   # 평균 대화 깊이 (Turns)
        })
        
    # 시도 횟수가 많은 순으로 정렬하여 반환
    return sorted(analysis_results, key=lambda x: x['total_attempts'], reverse=True)

def get_content_element_distribution():
    """성취기준별 질문 분포"""
    base_url, headers = get_supabase_config()
    resp = requests.get(f"{base_url}/conversations?select=content_element", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if not data:
            return []
        df = pd.DataFrame(data)
        if 'content_element' not in df or df.empty:
            return []
        df = df[df['content_element'] != 'N/A']
        counts = df['content_element'].value_counts()
        return [(index, count) for index, count in counts.items()]
    return []

def get_student_question_counts():
    """학생별 질문 횟수"""
    base_url, headers = get_supabase_config()
    resp = requests.get(f"{base_url}/conversations?select=student_id", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if not data:
            return []
        df = pd.DataFrame(data)
        if 'student_id' not in df or df.empty:
            return []
        counts = df['student_id'].value_counts()
        return [(index, count) for index, count in counts.items()]
    return []

# --- 연구용/기기 제한용 추가 함수 ---

def get_student_device(student_id: str):
    """학생에게 할당된 기기 조회"""
    base_url, headers = get_supabase_config()
    s_id = urllib.parse.quote(student_id)
    resp = requests.get(f"{base_url}/student_devices?select=device_id&student_id=eq.{s_id}", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            return data[0]["device_id"]
    return None

def register_student_device(student_id: str, device_id: str):
    """최초 로그인 학생의 기기 등록"""
    base_url, headers = get_supabase_config()
    data = {"student_id": student_id, "device_id": device_id}
    requests.post(f"{base_url}/student_devices", headers=headers, json=data)

def log_blocked_attempt(student_id: str, attempted_device_id: str):
    """차단된 로그인 시도 기록"""
    base_url, headers = get_supabase_config()
    data = {"student_id": student_id, "attempted_device_id": attempted_device_id}
    requests.post(f"{base_url}/blocked_logins", headers=headers, json=data)