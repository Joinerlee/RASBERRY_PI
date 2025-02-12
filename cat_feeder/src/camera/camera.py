# src/camera/camera.py
import os
import subprocess
from datetime import datetime
import time

class CameraController:
    def __init__(self):
        self.recording = False
        
    def record_segment(self, duration=5) -> str:
        """한 세그먼트 녹화"""
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'videos')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            # 임시 h264 파일
            temp_filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
            temp_filepath = os.path.join(save_dir, temp_filename)
            
            # 최종 MP4 파일
            final_filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            final_filepath = os.path.join(save_dir, final_filename)
            
            # 녹화
            subprocess.run([
                'libcamera-vid',
                '--width', '3840',
                '--height', '2160',
                '--ev', '1',           
                '--gain', '2',         
                '--brightness', '0.5',  
                '--contrast', '1.2',    
                '--framerate', '15',    
                '--codec', 'h264',
                '--timeout', str(duration * 1000),
                '--output', temp_filepath,
                '--quiet'
            ])
            
            # h264를 MP4로 변환
            subprocess.run(['ffmpeg', '-i', temp_filepath, '-c', 'copy', final_filepath, '-y', '-loglevel', 'quiet'])
            
            # 임시 파일 삭제
            os.remove(temp_filepath)
            
            print(f"세그먼트 녹화 완료: {final_filename}")
            return final_filepath
            
        except Exception as e:
            print(f"녹화 중 오류: {e}")
            return None

    def continuous_recording(self):
        """무한 분할 녹화"""
        try:
            print("연속 녹화를 시작합니다. 중지하려면 Ctrl+C를 누르세요.")
            while True:
                self.record_segment()
                
        except KeyboardInterrupt:
            print("\n녹화를 종료합니다.")

if __name__ == "__main__":
    camera = CameraController()
    camera.continuous_recording()