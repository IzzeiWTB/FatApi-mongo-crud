# Estágio 1: Imagem base com Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt
# --no-cache-dir: não armazena o cache do pip, reduzindo o tamanho da imagem
# --upgrade pip: garante que a versão mais recente do pip seja usada
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copia o restante do código da aplicação (a pasta 'app') para o diretório de trabalho
COPY ./app /app

# Expõe a porta 8000, que é a porta onde o Uvicorn irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner for executado
# uvicorn: servidor ASGI
# main:app: referencia o objeto 'app' no arquivo 'main.py'
# --host 0.0.0.0: permite que a aplicação seja acessível de fora do contêiner
# --port 8000: porta em que a aplicação vai rodar
# --reload: reinicia o servidor automaticamente quando detecta mudanças no código (ótimo para desenvolvimento)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
