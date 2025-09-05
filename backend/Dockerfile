FROM python:3.11-alpine

WORKDIR /app/backend

# 
COPY ./requirements.txt /app/backend/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/backend/requirements.txt

EXPOSE 80
# 
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
