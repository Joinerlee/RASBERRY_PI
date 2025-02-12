# src/camera/camera.py
import os
import subprocess
from datetime import datetime
import time

class CameraController:
    def __init__(self):
        self.recording = False
        
    def start_recording(self, duration=0) -> str:
        """영상 녹화 시작
        Args:
            duration (int): 녹화 시간(초). 0이면 무제한 녹화
        """
        try:
            # 저장 경로 설정
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'videos')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
            filepath = os.path.join(save_dir, filename)
            
            # libcamera-vid로 녹화 시작
            cmd = [
                'libcamera-vid',
                '--width', '3840',
                '--height', '2160',
                '--ev', '1',           
                '--gain', '2',         
                '--brightness', '0.5',  
                '--contrast', '1.2',    
                '--framerate', '30',    # 30fps
                '--codec', 'h264',
                '--output', filepath
            ]
            
            if duration > 0:
                cmd.extend(['--timeout', str(duration * 1000)])  # milliseconds
                
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
            
    def capture_image(self) -> str:
        """사진 촬영"""
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'images')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            subprocess.run([
                'libcamera-still',
                '--width', '3840',
                '--height', '2160',
                '--ev', '1',          
                '--gain', '2',         
                '--brightness', '0.5',  
                '--contrast', '1.2',    
                '--sharpness', '1.5',   
                '-o', filepath
            ])
            
            print(f"이미지 저장됨: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"촬영 중 오류: {e}")
            return None
            
# 테스트용 센서 시뮬레이션
def simulate_sensor():
    return True  # 실제 센서 구현 시 교체

# 테스트
if __name__ == "__main__":
    camera = CameraController()
    try:
        print("센서 감지 시작...")
        while True:
            if simulate_sensor():  # 센서가 감지되면
                if not camera.recording:
                    camera.start_recording()  # 녹화 시작
            else:
                if camera.recording:
                    camera.stop_recording()  # 녹화 정지
            time.sleep(0.1)  # 100ms 간격으로 체크
            
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
        if camera.recording:
            camera.stop_recording()