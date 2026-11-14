FROM mongo:8.0 AS mongo_cli
FROM ubuntu:24.04 AS ferramentas
ARG HTTP_PROXY
ARG HTTPS_PROXY
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client python3 ca-certificates libssl3t64 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=mongo_cli /usr/bin/mongosh /usr/bin/mongosh
WORKDIR /lab
USER 10001:10001
ENTRYPOINT ["python3", "scripts/executar.py"]

FROM ferramentas AS desenvolvimento
# Código fornecido pelo bind mount do Compose dev.

FROM ferramentas AS final
COPY --chown=10001:10001 exercicio-1/ exercicio-1/
COPY --chown=10001:10001 exercicio-2/ exercicio-2/
COPY --chown=10001:10001 exercicio-3/ exercicio-3/
COPY --chown=10001:10001 exercicio-4/01-consultas.js exercicio-4/01-consultas.js
COPY --chown=10001:10001 scripts/executar.py scripts/executar.py
COPY --chown=10001:10001 scripts/validar-isolamento.* scripts/
