# src/camera/camera.py

from picamera2 import Picamera2
import time
from datetime import datetime
import os
from config.settings import CAMERA_SETTINGS

class CameraController:
    def __init__(self):
        self.camera = Picamera2()
        # 카메라 기본 설정
        self.configure_camera()
        
    def configure_camera(self):
        """카메라 초기 설정"""
        # 카메라 설정
        config = self.camera.create_still_configuration(
            main={"size": (1920, 1080)},
            lores={"size": (640, 480)},
            display="lores"
        )
        self.camera.configure(config)
        
        # ISO 설정
        if hasattr(self.camera, 'set_controls'):
            self.camera.set_controls({"AnalogueGain": CAMERA_SETTINGS['ISO']})
            
    def start(self):
        """카메라 시작"""
        self.camera.start()
        # 카메라 안정화를 위한 대기
        time.sleep(2)
        
    def stop(self):
        """카메라 정지"""
        self.camera.stop()
        
    def capture_image(self) -> str:
        """사진 촬영 및 저장
        
        Returns:
            str: 저장된 이미지 파일 경로
        """
        try:
            # 이미지 저장 경로 설정
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'images')
            
            # 저장 폴더가 없다면 생성
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            # 파일명 생성 (timestamp 사용)
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            # 사진 촬영
            self.camera.capture_file(filepath)
            print(f"이미지 저장됨: {filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"이미지 촬영 중 오류 발생: {e}")
            return None

# 테스트 코드
if __name__ == "__main__":
    try:
        camera = CameraController()
        print("카메라 초기화 완료")
        
        camera.start()
        print("카메라 시작됨")
        
        # 테스트 촬영
        input("Enter를 누르면 사진을 촬영합니다...")
        filepath = camera.capture_image()
        
        if filepath:
            print(f"이미지가 성공적으로 저장되었습니다: {filepath}")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    
    finally:
        if 'camera' in locals():
            camera.stop()
            print("카메라 종료")