# src/api/feeding_reporter.py

import aiohttp
import asyncio
from datetime import datetime
from loguru import logger
from typing import Dict, Any

class FeedingReporter:
    def __init__(self, base_url: str = "http://your-backend-url/api"):
        self.base_url = base_url
        self.feeding_endpoint = f"{base_url}/feeding"
        
    async def report_feeding(self, feeding_data: Dict[str, Any]) -> Dict[str, Any]:
        """급식 결과를 백엔드에 전송
        
        Args:
            feeding_data (Dict[str, Any]): 급식 결과 데이터
            
        Returns:
            Dict[str, Any]: 서버 응답
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.feeding_endpoint,
                    json=feeding_data
                ) as response:
                    response_data = await response.json()
                    
                    if response.status == 200:
                        logger.info(f"급식 결과 전송 성공: {response_data}")
                    else:
                        logger.error(f"급식 결과 전송 실패: {response_data}")
                        
                    return {
                        "success": response.status == 200,
                        "status_code": response.status,
                        "response": response_data,
                        "timestamp": datetime.now().isoformat()
                    }
                    
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"급식 결과 전송 중 에러 발생: {error_result}")
            return error_result
            
# 메인 실행 코드
async def main():
    """테스트용 메인 함수"""
    feeder = FeederMotor()
    reporter = FeedingReporter()
    
    try:
        # 급식 실행
        feeding_result = feeder.feed()
        
        # 결과 전송
        if feeding_result["success"]:
            report_result = await reporter.report_feeding(feeding_result)
            print(f"Report result: {report_result}")
            
    finally:
        feeder.cleanup()

if __name__ == "__main__":
    asyncio.run(main())