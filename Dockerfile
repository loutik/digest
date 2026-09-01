FROM python:3.14-slim

RUN groupadd -r loutik && \
    useradd -r -g loutik -d /app -s /sbin/nologin loutik

WORKDIR /app

EXPOSE 8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG VERSION=0.0.0
ENV APP_VERSION=$VERSION

COPY --chown=loutik:loutik app/ ./

RUN mkdir -p var/html && chown -R loutik:loutik var/html

USER loutik

CMD ["python", "main.py"]