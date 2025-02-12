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
                
            # h264 파일로 먼저 저장
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
            self.filepath = os.path.join(save_dir, filename)
            
            # 녹화 시작
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
                '--output', self.filepath,
                '--quiet',
                '-n'
            ]
            
            self.process = subprocess.Popen(cmd, stderr=subprocess.DEVNULL)
            self.recording = True
            print(f"녹화 시작: {self.filepath}")
            return self.filepath
            
        except Exception as e:
            print(f"녹화 시작 중 오류: {e}")
            return None
            
    def stop_recording(self):
        """녹화 정지 및 MP4 변환"""
        if self.recording and self.process:
            self.process.terminate()
            self.process.wait()
            self.recording = False
            
            # h264를 MP4로 변환
            mp4_filepath = self.filepath.replace('.h264', '.mp4')
            subprocess.run(['ffmpeg', '-i', self.filepath, '-c', 'copy', mp4_filepath, '-y'], stderr=subprocess.DEVNULL)
            
            # h264 파일 삭제
            os.remove(self.filepath)
            
            print(f"녹화 종료 및 변환 완료: {mp4_filepath}")

if __name__ == "__main__":
    camera = CameraController()
    try:
        print("녹화를 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        camera.start_recording()
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n녹화를 종료합니다.")
        camera.stop_recording()