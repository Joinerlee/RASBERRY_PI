from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 설정
MAIN_BACKEND_URL = os.getenv('MAIN_BACKEND_URL')
API_VERSION = os.getenv('API_VERSION')

# GPIO 핀 설정
MOTOR_PINS = {
    'IN1': int(os.getenv('MOTOR_IN1_PIN')),
    'IN2': int(os.getenv('MOTOR_IN2_PIN')),
    'ENA': int(os.getenv('MOTOR_ENA_PIN'))
}

# 모터 설정
MOTOR_SPEED = int(os.getenv('MOTOR_SPEED'))
MOTOR_RUNTIME = float(os.getenv('MOTOR_RUNTIME'))

# 급식 설정
FEEDING_TIMES = os.getenv('FEEDING_TIMES').split(',')
PORTION_SIZE = float(os.getenv('PORTION_SIZE'))

# 카메라 설정
CAMERA_SETTINGS = {
    'ROTATION': int(os.getenv('CAMERA_ROTATION')),
    'ISO': int(os.getenv('CAMERA_ISO'))
}

# 디버그 모드
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# API 엔드포인트
def get_api_endpoint(endpoint: str) -> str:
    """API 엔드포인트 URL 생성"""
    return f"{MAIN_BACKEND_URL}/api/{API_VERSION}/{endpoint}"