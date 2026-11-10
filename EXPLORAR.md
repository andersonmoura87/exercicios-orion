# Explorar os containers

Execute os comandos a partir da raiz do repositório. As cinco stacks podem
funcionar simultaneamente. A API só possui rota `/` no exercício 1;
nos demais, comece por `/docs`, `/tarefas` ou `/health` no extra.

| Exercício/ambiente | Projeto Compose | Serviços | API | Swagger | pgAdmin |
|---|---|---|---|---|---|
| 1 | orion-ex1 | api | http://localhost:3000 | http://localhost:3000/docs | — |
| 2 | orion-ex2 | api, db | http://localhost:3001 | http://localhost:3001/docs | — |
| 3 dev | orion-ex3-dev | api, db | http://localhost:3002 | http://localhost:3002/docs | — |
| 3 prod | orion-ex3-prod | api, db | http://localhost:3003 | http://localhost:3003/docs | — |
| Extra dev | orion-exextra | api, db, pgadmin | http://localhost:3004 | http://localhost:3004/docs | http://localhost:8080 |

## Comandos de operação

Em PowerShell, na raiz:

```powershell
$ex1 = 'docker/exercicio-1/docker-compose.yml'
$ex2 = 'docker/exercicio-2/docker-compose.yml'
$dev = 'docker/exercicio-3/docker-compose.dev.yml'
$prod = 'docker/exercicio-3/docker-compose.prod.yml'
$extra = 'docker/exercicio-extra/docker-compose.yml'
```

| Ambiente | Logs ao vivo | Encerrar preservando os dados |
|---|---|---|
| 1 | `docker compose -f $ex1 logs -f` | `docker compose -f $ex1 down` |
| 2 | `docker compose -f $ex2 logs -f` | `docker compose -f $ex2 down` |
| 3 dev | `docker compose -f $dev logs -f` | `docker compose -f $dev down` |
| 3 prod | `docker compose -f $prod logs -f` | `docker compose -f $prod down` |
| Extra | `docker compose -f $extra logs -f` | `docker compose -f $extra down` |

Ctrl+C sai da visualização dos logs sem parar os containers. Acrescente `api`,
`db` ou `pgadmin` ao fim do comando para acompanhar apenas um serviço.
Use `docker compose -f $extra ps` para conferir o estado. Para iniciar novamente,
use `up -d --wait` com o mesmo arquivo. Para reconstruir, `up -d --build --wait`.
`down` preserva volumes; **não acrescente `-v`**, pois apagaria os dados.

## Roteiro curto

1. Abra http://localhost:3000 e confira `Hello from Docker!`. Depois abra o Swagger
   do extra em http://localhost:3004/docs.
2. Expanda **POST /tarefas**, clique em **Try it out**, envie
   `{"titulo":"Minha primeira tarefa no Swagger"}` e clique em **Execute**.
   Anote o `id` retornado com HTTP 201. Execute **GET /tarefas** e localize o id.
3. Abra http://localhost:8080. Use o email e a senha do `.env` do extra, sem
   compartilhá-los. A conexão **Orion - tarefas** foi cadastrada sem senha salva.
   Ao conectar, informe DB_PASS do mesmo `.env`. O host é `db`, porta `5432`,
   banco e usuário correspondem a DB_NAME e DB_USER. Se precisar cadastrar
   manualmente, use **Register > Server** e esses mesmos campos.
   Abra o **Query Tool** do banco e execute:

   ```sql
   SELECT id, titulo FROM tarefas ORDER BY id;
   ```

   Localize o mesmo id e título. Este pgAdmin acessa o banco do **extra**;
   os bancos dos outros projetos estão em redes separadas.
4. Em outro terminal, execute `docker compose -f $extra logs -f api`.
   Repita GET no Swagger e observe o acesso HTTP registrado.
5. Para experimentar reload, abra `docker/exercicio-3/api/app/main.py` e altere
   temporariamente `app = FastAPI(lifespan=lifespan)` para
   `app = FastAPI(title="Minha API dev", lifespan=lifespan)`.
   Salve e atualize http://localhost:3002/docs. Observe também
   `docker compose -f $dev logs -f api`. A porta 3003 de prod mantém o título
   anterior, pois usa o código da imagem. Restaure a linha original e salve.
   A API do extra também suporta reload, em sua própria pasta independente.
6. Confira persistência do extra:

   ```powershell
   docker compose -f $extra down
   docker compose -f $extra up -d --wait
   curl.exe -sS http://localhost:3004/tarefas
   ```

   A tarefa deve continuar presente. Você pode repetir com `$ex2`, `$dev` e `$prod`.
   Use sempre o mesmo arquivo para preservar o projeto e seu volume correspondente.

## O que cada container faz

`api` executa FastAPI pelo Uvicorn; recebe HTTP e faz consultas SQL. `db` executa
PostgreSQL e mantém dados no volume nomeado. `pgadmin` é a interface web de
administração do banco do extra e tem seu próprio volume para configurações.

O caminho é navegador → porta local publicada → API → `db:5432`, na rede do
projeto. Para administrar: navegador → porta 8080 → pgAdmin → `db:5432`.
O navegador não acessa PostgreSQL diretamente. `localhost` dentro de um container
é o próprio container; o nome `db` identifica o banco pela rede Compose.
