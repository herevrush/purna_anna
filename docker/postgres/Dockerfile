FROM postgres:16

LABEL maintainer="purna-team"
LABEL description="PostgreSQL 16 for the purna grocery store app"

# Copy init script; Postgres runs *.sql files in /docker-entrypoint-initdb.d
# on first startup (when the data directory is empty).
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql

# Default env vars — override via docker-compose or .env
ENV POSTGRES_DB=purna
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

EXPOSE 5432
