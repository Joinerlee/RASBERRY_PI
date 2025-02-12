
import time
from datetime import datetime
import RPi.GPIO as GPIO
import sys
sys.path.append('..')  # src 폴더로 가기 위해
from config.settings import MOTOR_PINS, MOTOR_SPEED, MOTOR_RUNTIME, FEEDING_TIMES

class FeederMotor:
    def __init__(self):
        # 환경변수에서 GPIO 핀 설정 가져오기
        self.in1 = MOTOR_PINS['IN1']
        self.in2 = MOTOR_PINS['IN2']
        self.ena = MOTOR_PINS['ENA']
        
        # 환경변수에서 모터 설정 가져오기
        self.speed = MOTOR_SPEED
        self.runtime = MOTOR_RUNTIME
        
        # GPIO 초기 설정
        self.setup_gpio()
        
    def setup_gpio(self):
        """GPIO 핀 설정"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        
        # PWM 설정
        self.pwm = GPIO.PWM(self.ena, 100)  # 100Hz 주파수
        self.pwm.start(0)
        
    def feed(self) -> dict:
        """사료 배급 실행"""
        try:
            feeding_time = datetime.now()
            
            # 모터 작동
            self.pwm.ChangeDutyCycle(self.speed)  # 설정된 속도로 작동
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            
            # 설정된 시간동안 작동
            time.sleep(self.runtime)
            
            # 모터 정지
            self.pwm.ChangeDutyCycle(0)
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
            
            return {
                "success": True,
                "timestamp": feeding_time.isoformat(),
                "motor_runtime": self.runtime
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def cleanup(self):
        """GPIO 설정 초기화"""
        self.pwm.stop()
        GPIO.cleanup([self.in1, self.in2, self.ena])


class FeedingScheduler:
    def __init__(self):
        self.feeder = FeederMotor()
        self.feeding_times = FEEDING_TIMES
        
    def should_feed(self) -> bool:
        """현재 시간이 급식 시간인지 확인"""
        current_time = datetime.now().strftime("%H:%M")
        return current_time in self.feeding_times
        
    def run_scheduled_feeding(self):
        """정해진 시간에 급식 실행"""
        if self.should_feed():
            return self.feeder.feed()
        return None
        
    def cleanup(self):
        self.feeder.cleanup()


# 테스트 코드
if __name__ == "__main__":
    try:
        feeder = FeederMotor()
        result = feeder.feed()
        print(f"Feeding result: {result}")
        
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    
    finally:
        feeder.cleanup()