#!/bin/bash
# Render에서 FastAPI 앱 실행용
uvicorn main:app --host 0.0.0.0 --port $PORT
