# src/motor/feeder.py

import time
from datetime import datetime
import RPi.GPIO as GPIO
import json
import os
from config.settings import MOTOR_PINS, MOTOR_SPEED, MOTOR_RUNTIME, FEEDING_TIMES

class FeederMotor:
    def __init__(self):
        self.in1 = MOTOR_PINS['IN1']
        self.in2 = MOTOR_PINS['IN2']
        self.ena = MOTOR_PINS['ENA']
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
            self.pwm.ChangeDutyCycle(MOTOR_SPEED)
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            
            # 설정된 시간동안 작동
            time.sleep(MOTOR_RUNTIME)
            
            # 모터 정지
            self.pwm.ChangeDutyCycle(0)
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
            
            result = {
                "success": True,
                "timestamp": feeding_time.isoformat(),
                "motor_runtime": MOTOR_RUNTIME
            }
            
            # 결과 저장
            self.save_result(result)
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.save_result(error_result)
            return error_result
    
    def save_result(self, result: dict):
        """급식 결과를 JSON 파일로 저장"""
        # logs 폴더 경로
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        
        # logs 폴더가 없다면 생성
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 오늘 날짜로 파일명 생성
        filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}_feeding_log.json")
        
        # 기존 로그 읽기
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
        else:
            logs = []
        
        # 새로운 결과 추가
        logs.append(result)
        
        # 저장
        with open(filename, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def cleanup(self):
        """GPIO 설정 초기화"""
        self.pwm.stop()
        GPIO.cleanup([self.in1, self.in2, self.ena])


if __name__ == "__main__":
    try:
        feeder = FeederMotor()
        result = feeder.feed()
        print(f"Feeding result: {result}")
        
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        if 'feeder' in locals():
            feeder.cleanup()