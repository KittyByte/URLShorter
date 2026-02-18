FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./pyproject.toml pyproject.toml

RUN uv pip install --system --no-cache-dir --upgrade -r pyproject.toml

COPY . .

# ENTRYPOINT ["./entrypoint.sh"]