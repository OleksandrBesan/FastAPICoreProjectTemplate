FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir poetry
RUN pip install --no-cache-dir gunicorn
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
COPY . /app
EXPOSE 8000
CMD ["gunicorn", "--chdir", "src",  "-c", "gunicorn_config.py"  ,  "--worker-class",  "uvicorn.workers.UvicornWorker",  "--reload" ,  "main:app"] 
