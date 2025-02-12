# src/camera/camera.py
import os
import subprocess
from datetime import datetime
import time

class CameraController:
   def __init__(self):
       self.recording = False
       
   def start_recording(self, duration=5) -> str:  # 기본값 5초로 설정
       """영상 녹화 시작
       Args:
           duration (int): 녹화 시간(초)
       """
       try:
           # 저장 경로 설정
           save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'videos')
           if not os.path.exists(save_dir):
               os.makedirs(save_dir)
               
           filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
           filepath = os.path.join(save_dir, filename)
           
           # libcamera-vid로 녹화 시작 (4K, 15fps)
           cmd = [
               'libcamera-vid',
               '--width', '3840',
               '--height', '2160',
               '--ev', '1',           
               '--gain', '2',         
               '--brightness', '0.5',  
               '--contrast', '1.2',    
               '--framerate', '15',    # 15fps로 변경
               '--codec', 'h264',
               '--timeout', str(duration * 1000),  # 5초 (밀리초 단위)
               '--output', filepath
           ]
               
           self.recording_process = subprocess.Popen(cmd)
           self.recording = True
           print(f"녹화 시작: {filepath}")
           return filepath
           
       except Exception as e:
           print(f"녹화 시작 중 오류: {e}")
           return None
           
   def stop_recording(self):
       """녹화 정지"""
       if self.recording and hasattr(self, 'recording_process'):
           self.recording_process.terminate()
           self.recording = False
           print("녹화 정지")

# 테스트
if __name__ == "__main__":
   camera = CameraController()
   try:
       print("5초 녹화를 시작합니다...")
       camera.start_recording()  # 5초 녹화
       time.sleep(6)  # 녹화가 완전히 끝날 때까지 대기
           
   except KeyboardInterrupt:
       print("\n프로그램을 종료합니다.")
       if camera.recording:
           camera.stop_recording()