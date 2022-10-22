FROM gcr.io/distroless/python3

WORKDIR /app

RUN \
    pip install -r requirements.txt \

COPY --from=docker-minifier /app /app

CMD ["python", "main.py"]
