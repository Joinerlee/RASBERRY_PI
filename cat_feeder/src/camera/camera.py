import picamera
import os
from datetime import datetime
import time

class CameraController:
    def __init__(self):
        self.camera = None
        self.recording = False
        self.filepath = None
        
    def start_recording(self) -> str:
        """연속 녹화 시작"""
        try:
            # 저장 디렉토리 생성
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'videos')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            # 파일명 생성
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
            self.filepath = os.path.join(save_dir, filename)
            
            # 카메라 초기화
            self.camera = picamera.PiCamera()
            self.camera.resolution = (1920, 1080)
            self.camera.framerate = 30
            
            # 녹화 시작
            self.camera.start_recording(self.filepath)
            self.recording = True
            print(f"녹화 시작: {self.filepath}")
            return self.filepath
            
        except Exception as e:
            print(f"녹화 시작 중 오류: {e}")
            return None
            
    def stop_recording(self):
        """녹화 정지"""
        if self.recording and self.camera:
            try:
                self.camera.stop_recording()
                self.camera.close()
                print(f"녹화 종료: {self.filepath}")
            except Exception as e:
                print(f"녹화 종료 중 오류: {e}")
            finally:
                self.recording = False
                self.camera = None

    def __del__(self):
        """소멸자: 인스턴스 삭제 시 녹화 중지"""
        if self.recording:
            self.stop_recording()

if __name__ == "__main__":
    camera = CameraController()
    try:
        print("녹화를 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        camera.start_recording()
        
        # 메인 루프
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n녹화를 종료합니다.")
        camera.stop_recording()
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        if camera.recording:
            camera.stop_recording()
