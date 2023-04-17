import subprocess

fastapi_process = subprocess.Popen(['uvicorn', 'app:app', '--reload', '--host=0.0.0.0', '--port=8000'])
mongo_process = subprocess.Popen(['python3', 'result.py'])


fastapi_process.wait()
mongo_process.wait()

