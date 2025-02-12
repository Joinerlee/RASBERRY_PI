# src/camera/camera.py
import os
import subprocess
from datetime import datetime
import time

class CameraController:
    def __init__(self):
        self.recording = False
        self.process = None
        
    def start_recording(self) -> str:
        """연속 녹화 시작"""
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'videos')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            filepath = os.path.join(save_dir, filename)
            
            # 녹화 시작 (타임아웃 없이)
            cmd = [
                'libcamera-vid',
                '--width', '3840',
                '--height', '2160',
                '--ev', '1',           
                '--gain', '2',         
                '--brightness', '0.5',  
                '--contrast', '1.2',    
                '--framerate', '15',    
                '--codec', 'h264',
                '--output', filepath,
                '--quiet',
                '-n'
            ]
            
            self.process = subprocess.Popen(cmd, stderr=subprocess.DEVNULL)
            self.recording = True
            print(f"녹화 시작: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"녹화 시작 중 오류: {e}")
            return None
            
    def stop_recording(self):
        """녹화 정지"""
        if self.recording and self.process:
            self.process.terminate()
            self.process.wait()
            self.recording = False
            print("녹화 종료")

if __name__ == "__main__":
    camera = CameraController()
    try:
        print("녹화를 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        camera.start_recording()
        while True:
            time.sleep(1)  # CPU 사용량을 줄이기 위한 대기
            
    except KeyboardInterrupt:
        print("\n녹화를 종료합니다.")
        camera.stop_recording()