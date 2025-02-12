import os
import subprocess
from datetime import datetime
import time
import signal

class CameraController:
    def __init__(self):
        self.recording = False
        self.process = None
        self.filepath = None
        
    def start_recording(self) -> str:
        """연속 녹화 시작"""
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'videos')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
            self.filepath = os.path.join(save_dir, filename)
            
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
                '--inline',  # 헤더 정보 포함
                '--flush',   # 버퍼 즉시 쓰기
                '--output', self.filepath,
                '--quiet',
                '-n'
            ]
            
            # 이전 프로세스가 있다면 종료
            if self.process:
                self.stop_recording()
            
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
            try:
                # SIGINT 시그널 전송
                self.process.send_signal(signal.SIGINT)
                
                # 프로세스 종료 대기
                self.process.wait(timeout=5)
                
                # 파일 저장 완료 대기
                time.sleep(1)
                
                if self.filepath and os.path.exists(self.filepath):
                    # 파일 크기 확인
                    if os.path.getsize(self.filepath) == 0:
                        raise Exception("빈 비디오 파일")
                        
                    # MP4 변환
                    mp4_filepath = self.filepath.replace('.h264', '.mp4')
                    convert_cmd = [
                        'ffmpeg',
                        '-i', self.filepath,
                        '-c', 'copy',
                        mp4_filepath,
                        '-y'
                    ]
                    
                    subprocess.run(convert_cmd, check=True, stderr=subprocess.DEVNULL)
                    
                    # 원본 파일 삭제
                    os.remove(self.filepath)
                    print(f"녹화 종료 및 변환 완료: {mp4_filepath}")
                else:
                    print("녹화 파일이 생성되지 않았습니다.")
                    
            except subprocess.TimeoutExpired:
                print("프로세스 종료 시간 초과")
                self.process.kill()
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg 변환 실패: {e}")
            except Exception as e:
                print(f"처리 중 오류: {e}")
            finally:
                self.recording = False
                self.process = None

    def __del__(self):
        """소멸자: 인스턴스 삭제 시 녹화 중지"""
        if self.recording:
            self.stop_recording()

def signal_handler(signum, frame):
    """시그널 핸들러"""
    print("\n녹화를 종료합니다.")
    if camera.recording:
        camera.stop_recording()
    exit(0)

if __name__ == "__main__":
    camera = CameraController()
    
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("녹화를 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        camera.start_recording()
        
        # 메인 루프
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        if camera.recording:
            camera.stop_recording()
import os
import subprocess
from datetime import datetime
import time
import signal

class CameraController:
    def __init__(self):
        self.recording = False
        self.process = None
        self.filepath = None
        
    def start_recording(self) -> str:
        """연속 녹화 시작"""
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'videos')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
            self.filepath = os.path.join(save_dir, filename)
            
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
                '--inline',  # 헤더 정보 포함
                '--flush',   # 버퍼 즉시 쓰기
                '--output', self.filepath,
                '--quiet',
                '-n'
            ]
            
            # 이전 프로세스가 있다면 종료
            if self.process:
                self.stop_recording()
            
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
            try:
                # SIGINT 시그널 전송
                self.process.send_signal(signal.SIGINT)
                
                # 프로세스 종료 대기
                self.process.wait(timeout=5)
                
                # 파일 저장 완료 대기
                time.sleep(1)
                
                if self.filepath and os.path.exists(self.filepath):
                    # 파일 크기 확인
                    if os.path.getsize(self.filepath) == 0:
                        raise Exception("빈 비디오 파일")
                        
                    # MP4 변환
                    mp4_filepath = self.filepath.replace('.h264', '.mp4')
                    convert_cmd = [
                        'ffmpeg',
                        '-i', self.filepath,
                        '-c', 'copy',
                        mp4_filepath,
                        '-y'
                    ]
                    
                    subprocess.run(convert_cmd, check=True, stderr=subprocess.DEVNULL)
                    
                    # 원본 파일 삭제
                    os.remove(self.filepath)
                    print(f"녹화 종료 및 변환 완료: {mp4_filepath}")
                else:
                    print("녹화 파일이 생성되지 않았습니다.")
                    
            except subprocess.TimeoutExpired:
                print("프로세스 종료 시간 초과")
                self.process.kill()
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg 변환 실패: {e}")
            except Exception as e:
                print(f"처리 중 오류: {e}")
            finally:
                self.recording = False
                self.process = None

    def __del__(self):
        """소멸자: 인스턴스 삭제 시 녹화 중지"""
        if self.recording:
            self.stop_recording()

def signal_handler(signum, frame):
    """시그널 핸들러"""
    print("\n녹화를 종료합니다.")
    if camera.recording:
        camera.stop_recording()
    exit(0)

if __name__ == "__main__":
    camera = CameraController()
    
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("녹화를 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        camera.start_recording()
        
        # 메인 루프
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        if camera.recording:
            camera.stop_recording()
