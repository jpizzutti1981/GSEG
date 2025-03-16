@echo off
cd /d C:\Users\Jorge\gestao_ocorrencias
call .\venv\Scripts\activate

start cmd /k "celery -A gestao_ocorrencias worker --loglevel=info --pool=solo"
start cmd /k "celery -A gestao_ocorrencias beat --loglevel=info"
exit
