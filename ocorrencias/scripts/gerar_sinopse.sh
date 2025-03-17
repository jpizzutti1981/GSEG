#!/bin/bash
# Ativar ambiente virtual no Render
source /opt/render/project/src/.venv/bin/activate

# Ir para o diretório do projeto
cd /opt/render/project/src

# Executar o comando Django para gerar e enviar a sinopse
python manage.py enviar_sinopse
