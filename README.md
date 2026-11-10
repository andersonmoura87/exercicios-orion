# exercicios-orion

Exercícios práticos de Docker com FastAPI, Uvicorn e PostgreSQL.
O enunciado completo (seis páginas) está em [docs/enunciados/Docker.pdf](docs/enunciados/Docker.pdf).
O PDF original na raiz foi preservado.

Requisitos locais: Docker Desktop com engine Linux e Docker Compose v2.
Cada pasta é autossuficiente; siga seu README:

| Exercício | Guia | API | Outros acessos |
|---|---|---|---|
| 1 | [Hello](docker/exercicio-1/README.md) | http://localhost:3000 | /docs |
| 2 | [API e banco](docker/exercicio-2/README.md) | http://localhost:3001 | /docs |
| 3 | [Dev e prod](docker/exercicio-3/README.md) | http://localhost:3002 e :3003 | /docs |
| Extra | [Stack completa](docker/exercicio-extra/README.md) | http://localhost:3004 | pgAdmin em http://localhost:8080 |

Um bind mount compartilha arquivos do host com o container e permite editar o
código em dev. Um volume nomeado armazena os dados fora da camada descartável
do container. Cada projeto Compose dá seu prefixo aos volumes e à network `app`,
que permite comunicação por nomes de serviço. `healthcheck` mede prontidão;
`depends_on` com `service_healthy` ordena a inicialização. A API abre conexões
com `db:5432`; o pgAdmin usa o mesmo endereço. O navegador acessa as portas
publicadas no host. `down` remove containers e redes; `down -v` também apaga dados.

## Entrega

O fluxo do PDF é: branch de trabalho, pull request para `main`, revisão e aprovação
por outra pessoa, e envio do link do repositório GitHub ao mentor responsável.
Este trabalho usa `feat/exercicios-docker`. Não houve push, merge ou aprovação de PR.
Os commits usam datas reais; não foi simulado trabalho em dias anteriores.
O diretório local mantém o nome existente; ao criar o remoto, use `exercicios-orion`.

Sugestão de título de PR: **Implementa exercícios de Docker com FastAPI e PostgreSQL**.

Sugestão de descrição:
> Adiciona quatro exercícios independentes: Hello na porta 3000, tarefas com
> PostgreSQL persistente, ambientes dev/prod isolados e stack com pgAdmin e health.
> Inclui comandos PowerShell e explicações de rede, persistência e reload.
> Consulte VALIDACAO.md para as verificações executadas e limitações.

## Confira sua compreensão

Validação local opcional (requer Python 3.12, executada a partir da raiz):

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r scripts/requirements.txt
.venv/Scripts/python.exe scripts/validar_local.py
```

Esse script usa TestClient e falhas simuladas; não substitui subir os containers.
O relatório [VALIDACAO.md](VALIDACAO.md) distingue testes locais e testes Docker.

1. Por que DB_HOST é `db` e não `localhost`?
2. O que acontece com as tarefas após `down` e após `down -v`?
3. Como o bind mount e o reload trabalham juntos em dev?
4. Como os nomes de projeto evitam compartilhar dados entre dev e prod?
5. Por que o healthcheck inicial não substitui tratar falhas do banco nas rotas?
