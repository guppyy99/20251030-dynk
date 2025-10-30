"""Railway 배포용 시작 스크립트"""
import os
import subprocess
import sys

# Railway PORT 환경 변수 확인
port = os.environ.get("PORT", "8501")

# Streamlit 실행
cmd = [
    sys.executable,
    "-m",
    "streamlit",
    "run",
    "src/dashboard/streamlit_app.py",
    "--server.port", port,
    "--server.address", "0.0.0.0",
    "--server.headless", "true"
]

subprocess.run(cmd)

