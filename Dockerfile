FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /workdir

# Copy requirements.txt first for better cache on later pushes and install dependencies
COPY requirements.txt /workdir/requirements.txt
RUN pip install -r /workdir/requirements.txt

# Copy the rest of the code
COPY . /workdir/

EXPOSE 8000

# CMD ["uvicorn", "--app-dir", "/workdir/app","main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
