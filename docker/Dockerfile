FROM python:3.10-slim

WORKDIR /bot
COPY . /bot
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "examBot.py"]