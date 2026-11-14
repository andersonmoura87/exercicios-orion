# exercicios-orion

Exercícios práticos de Docker com FastAPI, Uvicorn e PostgreSQL.
O enunciado do curso foi consultado localmente. Seu PDF não é redistribuído
neste repositório público. Os arquivos PDF são ignorados pelo Git.

Requisitos locais: Docker Desktop com engine Linux e Docker Compose v2.
Para explorar as stacks e acompanhar os logs, siga [EXPLORAR.md](EXPLORAR.md).
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

## Rede durante o build

Os Compose aceitam BUILD_HTTP_PROXY e BUILD_HTTPS_PROXY no `.env` de cada
exercício. São opcionais e usados apenas como argumentos predefinidos de build
do Docker, sem ENV no Dockerfile nem proxy na execução das APIs.
Em redes com acesso direto, deixe ambos vazios. Neste computador, foi validado
o proxy interno existente do Docker Desktop: `http://http.docker.internal:3128`.
Somente os `.env` locais receberam esse endereço; os exemplos continuam vazios.
O host acessava o PyPI, mas containers/builds sem proxy tinham timeout IPv4 e
ausência de rota IPv6. Com proxy, HTTPS e os cinco builds funcionaram mantendo
a verificação TLS. Não houve mudança global de Docker, firewall, VPN ou proxy.
Não use `trusted-host` nem desative TLS. Se for necessário um proxy com
autenticação, não versione suas credenciais.

## Entrega

O fluxo do PDF é: branch de trabalho, pull request para `main`, revisão e aprovação
por outra pessoa, e envio do link do repositório GitHub ao mentor responsável.
Este trabalho usa `feat/exercicios-docker`, com pull request para `main`.
A revisão e aprovação devem ser realizadas por outra pessoa, antes de qualquer merge.
Os commits usam datas reais; não foi simulado trabalho em dias anteriores.
Esta é uma cópia de publicação com o PDF removido de todo o histórico. O repositório
local original, o material do curso e os containers foram preservados.
Mensagens, autores e datas dos commits originais foram mantidos; os hashes mudaram.

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
