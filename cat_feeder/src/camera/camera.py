# src/camera/camera.py
import os
import subprocess
from datetime import datetime

class CameraController:
   def __init__(self):
       pass
       
   def start_preview(self):
       """libcamera로 프리뷰 시작"""
       try:
           # libcamera-hello로 프리뷰
           subprocess.run(['libcamera-hello', '-t', '0'])
       except Exception as e:
           print(f"프리뷰 시작 중 오류: {e}")
           
   def capture_image(self) -> str:
       """사진 촬영"""
       try:
           # 저장 경로 설정
           save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'images')
           if not os.path.exists(save_dir):
               os.makedirs(save_dir)
               
           filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
           filepath = os.path.join(save_dir, filename)
           
           # libcamera-still로 4K 해상도 촬영
           subprocess.run([
               'libcamera-still',
               '--width', '3840',
               '--height', '2160',
               '--ev', '1',           # 노출 보정
               '--gain', '2',         # 게인
               '--brightness', '0.5',  # 밝기
               '--contrast', '1.2',    # 대비
               '--sharpness', '1.5',   # 선명도
               '-o', filepath
           ])
           
           print(f"이미지 저장됨: {filepath}")
           return filepath
           
       except Exception as e:
           print(f"촬영 중 오류: {e}")
           return None

if __name__ == "__main__":
   camera = CameraController()
   try:
       print("프리뷰를 시작합니다...")
       camera.start_preview()
       
   except KeyboardInterrupt:
       print("\n프리뷰를 종료합니다.")