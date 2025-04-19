FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8501

CMD sh -c "streamlit run app.py --server.port=${PORT} --server.enableCORS=false"

