#!/bin/bash
cd /home/render/project/src  # 🔹 Caminho do projeto no servidor Render
source venv/bin/activate  # 🔹 Ativa o ambiente virtual
python manage.py enviar_sinopse  # 🔹 Executa o comando Django
