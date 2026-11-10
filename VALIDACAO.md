# Verificações realizadas

## Cópia de publicação sem o material do curso

Esta cópia foi preparada com autorização para retirar os PDFs de todo o histórico.
As seções anteriores, abaixo, registram verificações no repositório local original;
as referências ao PDF descrevem o material consultado localmente e não um arquivo
disponível nesta cópia pública. O bloqueio anterior de publicação foi resolvido
pela criação desta cópia separada, sem autorização de redistribuição do PDF.

Os sete commits originais foram reconstruídos preservando suas mensagens,
autores, datas e relações de ancestralidade. Os únicos ajustes nessas árvores
foram remover os dois caminhos do PDF e incluir `*.pdf`/`*.PDF` no `.gitignore`.
O histórico público contém somente main como base e feat/exercicios-docker com
as implementações. Não foram incluídos refs de backup, branches auxiliares,
tags ou os objetos antigos que continham o PDF. O repositório original permanece
intacto, assim como os containers e volumes existentes.

Verificações executadas nesta cópia: comparação dos sete pares de commits
confirmou mensagens, autores e datas idênticos, com o código preservado em cada
árvore; inspeção de todos os objetos Git confirmou ausência de conteúdo PDF;
inspeção das refs confirmou somente as duas branches necessárias. A auditoria
por padrões em 41 blobs históricos não encontrou indícios de segredos; `.env`,
caches e temporários não estão no histórico. Os testes de `validar_local.py`
passaram, assim como as cinco configurações Compose usando `.env.example` com
proxies vazios. Não foi executado novo build ou reinício de containers nesta etapa.

## Preparação da entrega no GitHub

Verificações desta etapa, sem reiniciar containers nem modificar dados:

- Branch `feat/exercicios-docker`; `main` em `5340a30`, anterior às implementações.
  O diff para main contém os quatro exercícios e os guias, e não apenas documentação.
- Nenhum remote existente. Conta GitHub autenticada: `andersonmoura87`.
  A consulta a `andersonmoura87/exercicios-orion` retornou 404 (repositório ausente).
- Histórico auditado: 27 blobs únicos; sem achados nas buscas por tokens conhecidos,
  chaves privadas e atribuições de senhas fora dos valores de demonstração.
  Essa inspeção por padrões não equivale a garantia absoluta de ausência de segredos.
  `.env`, venv, cache e temporários ausentes dos caminhos históricos.
- Cinco Compose válidos com os `.env` locais; renderização com `.env.example`
  confirmou HTTP_PROXY/HTTPS_PROXY vazios, portanto o proxy interno não é obrigatório.
  Um build em outro computador não foi executado; sua rede ainda precisa acessar PyPI.
- `scripts/validar_local.py` passou; `git diff --check` sem erros.
- Cinco Swagger responderam HTTP 200; Hello exato, `/health` 200/status ok e login
  do pgAdmin HTTP 200 confirmados novamente pelos containers existentes.
- Dez containers permaneceram em execução; quatro bancos healthy; nenhum volume
  removido ou serviço reiniciado nesta etapa.

**Publicação suspensa:** o PDF do curso está no commit inicial `5340a30`, ancestral
de ambas as branches. Uma exclusão posterior não remove o PDF do histórico público.
Não há autorização clara de redistribuição. Para respeitar a preservação do
histórico e a restrição do PDF simultaneamente, a criação/publicação do remoto e
do PR não foram realizadas. O usuário confirmou que não tem autorização e pediu
para manter a publicação suspensa. Não houve rebase, reset, force push ou alteração
de autores/datas. O corpo proposto do PR foi preparado localmente.

## Atualização: APIs executando nos containers

Data local: 09/11/2026 (America/Sao_Paulo). Esta seção substitui as pendências
de execução do registro anterior, preservado abaixo como histórico.
Branch confirmada: `feat/exercicios-docker`; árvore inicialmente sem alterações.
Não foram criados commits, push, merge ou PR nesta etapa.

### Diagnóstico e correção da rede

| Verificação executada | Resultado observado |
|---|---|
| Host: HTTPS para https://pypi.org/simple/fastapi/ | HTTP 200 |
| Container Python oficial: resolução de pypi.org | DNS retornou endereços IPv4 e IPv6 |
| Container: TCP direto ao PyPI | IPv4: timeout; IPv6: Errno 101 / Network is unreachable |
| BuildKit: HTTPS sem proxy | Falhou com Network is unreachable; DNS funcionou |
| Configuração pip na imagem base | Sem pip.conf e sem override de índice ou proxy |
| Inspeção do Docker Desktop | Engine já informava proxy interno http.docker.internal:3128 |
| Container: HTTPS pelo proxy interno | HTTP 200 com validação TLS |
| BuildKit: HTTPS com HTTP_PROXY/HTTPS_PROXY como build args | HTTP 200 com validação TLS |
| Builds/up dos cinco ambientes | Todos concluídos com sucesso |

O erro não era falha de DNS nem de certificado. O caminho direto de saída dos
containers/builds falhava, enquanto o proxy interno existente funcionava.
Isso não identifica qual componente de rede do Windows bloqueia o caminho direto;
não foi necessário alterar esse componente para executar os exercícios.

Correção restrita ao projeto: os cinco Compose passam BUILD_HTTP_PROXY e
BUILD_HTTPS_PROXY opcionais do `.env` como argumentos predefinidos de build.
Os `.env` locais foram complementados sem sobrescrever os demais valores.
Os `.env.example` deixam os proxies vazios. Nenhum Dockerfile declara ENV de
proxy. A inspeção das imagens/containers confirmou ausência de proxy no ambiente
de execução das APIs. Não se alterou configuração global do Docker, Windows,
firewall, VPN ou proxy; TLS permaneceu habilitado, sem trusted-host.

### Verificações de execução

Todas as chamadas HTTP abaixo atingiram as APIs nos containers pelas portas
publicadas. O host executou somente o cliente de validação, sem servidor Python.

| Requisito | Procedimento executado | Resultado |
|---|---|---|
| Docker/Compose | version, compose version e inventário de containers | Engine 28.5.1 e Compose v2.40.0 disponíveis |
| Portas | Listeners Windows e inventário Docker antes do up | 3000–3004 e 8080 livres; nenhum ajuste de porta necessário |
| Compose | config --quiet para cada arquivo, antes de build/up | Cinco configurações válidas, sem imprimir credenciais |
| Exercício 1 | GET / e comparação de bytes | HTTP 200; exatamente Hello from Docker! |
| Swagger | GET /docs em 3000, 3001, 3002, 3003 e 3004 | HTTP 200 nos cinco ambientes |
| CRUD básico | POST /tarefas e GET /tarefas em ex2, dev, prod e extra | POST 201 e a mesma tarefa presente no GET em cada banco |
| Validação de entrada | POST com título contendo somente espaços | HTTP 422 nos quatro ambientes com banco |
| Usuário da API | docker compose exec api id -u em cada ambiente | UID 10001 em todos |
| Dev/prod: configuração efetiva | docker inspect de Cmd e Mounts | Dev com --reload e bind mount; prod sem --reload e sem bind mount do código |
| Dev/prod: dados e volumes | Tarefas distintas; consulta cruzada e inspeção de volumes | Tarefa de dev ausente em prod e vice-versa; volumes distintos |
| Reload real | Alteração temporária do título FastAPI em dev e extra; consulta a /openapi.json | Mudança observada sem rebuild; prod manteve título original |
| Restauração do código | finally restaurou bytes originais; nova consulta ao título; git diff dos dois main.py | Originais restaurados, sem diff; APIs responderam com título original |
| Health com banco disponível | GET extra /health | HTTP 200 e {"status":"ok"} |
| Health com banco indisponível | stop db do extra; GET /health | HTTP 503 e {"detail":"Banco indisponível"}, sem detalhes internos |
| Recuperação | up do extra e novo GET /health | HTTP 200 restaurado |
| Persistência ex2 | Criar tarefa; down; up -d --wait; consultar tarefa | ID 1, Explorar ex2 375305ad preservado |
| Persistência dev | Mesmo procedimento usando Compose dev | ID 1, Explorar dev 375305ad preservado |
| Persistência prod | Mesmo procedimento usando Compose prod | ID 1, Explorar prod 375305ad preservado |
| Persistência extra | Mesmo procedimento usando Compose extra | ID 4, Explorar extra 375305ad preservado; dados anteriores mantidos |
| pgAdmin web | GET /login após os reinícios | HTTP 200 na porta 8080 |
| pgAdmin/banco | Driver psycopg dentro do container pgAdmin consultou db:5432 | Mesmo id/título da tarefa criada pela API do extra confirmado |
| Cadastro pgAdmin | setup.py load-servers; leitura do cadastro SQLite para o usuário configurado | Orion - tarefas cadastrado sem senha salva; importação sem substituir outros cadastros |
| Estado final | docker ps e consultas HTTP finais | Dez containers em execução; quatro bancos healthy |

Nos testes de persistência foi usado somente `down`, sem `-v`. Não houve prune,
limpeza de cache ou exclusão de imagens/volumes. Não foram alterados recursos de
outros projetos. As portas dos bancos não foram publicadas no host nesta etapa.
Os testes de reinício e falha terminaram com os serviços restaurados e em execução.

O cadastro do pgAdmin e a consulta pelo driver do seu container foram verificados;
login e execução manual pelo Query Tool na interface gráfica ficam para sua
exploração, conforme [EXPLORAR.md](EXPLORAR.md). Isso não foi declarado como
teste de interface executado. Não há bloqueio de build ou execução pendente.

### Estado entregue

| Ambiente | Projeto | Containers em execução | URL principal |
|---|---|---|---|
| 1 | orion-ex1 | api | http://localhost:3000 |
| 2 | orion-ex2 | api; db healthy | http://localhost:3001/docs |
| 3 dev | orion-ex3-dev | api; db healthy | http://localhost:3002/docs |
| 3 prod | orion-ex3-prod | api; db healthy | http://localhost:3003/docs |
| Extra | orion-exextra | api; db healthy; pgadmin | http://localhost:3004/docs e http://localhost:8080 |

## Registro anterior: antes da correção de rede

Data local: 09/11/2026 (America/Sao_Paulo). O PDF foi extraído integralmente:
seis páginas lidas antes da implementação. Nenhum arquivo original foi removido.

Docker Engine 28.5.1 e Compose v2.40.0 estavam disponíveis via Docker Desktop
(contexto desktop-linux), fora das restrições de acesso do sandbox.

| Requisito | Arquivos | Validação | Resultado |
|---|---|---|---|
| Enunciado e organização | docs/enunciados/Docker.pdf; docker/exercicio-* | Leitura das seis páginas e inspeção dos arquivos | OK; original na raiz preservado |
| Compose independente | Os cinco arquivos docker-compose*.yml | docker compose -f ARQUIVO config --quiet com .env local | OK, sem imprimir credenciais |
| Hello exato | exercicio-1/api/app/main.py | GET com TestClient; comparação de bytes | OK: Hello from Docker! |
| Imagem leve, cache e usuário | Cada api/Dockerfile e .dockerignore | Inspeção: slim, requirements antes do código, USER app | OK estático; runtime dos containers da API pendente |
| Tarefas e SQL parametrizado | Exercícios 2, 3 e extra: main.py/database.py | APIs locais via TestClient com PostgreSQL real em Docker; POST 201 seguido de GET | OK para os três; texto semelhante a SQL persistido como dado |
| Validação e falhas | scripts/validar_local.py | Vazio, espaços, limite, tipo e campo ausente; falhas simuladas do banco | OK: 422 e 503 sem detalhes internos |
| Persistência | Extra: volume postgres_data | Primeiro registro temporário e depois três tarefas; down/up sem -v e SELECT | OK: registro preservado; três tarefas preservadas. Outros projetos não testados em runtime |
| Dev/prod | Exercício 3: Dockerfile e dois Compose | Parse YAML: targets, portas e projetos diferentes, sem mount/reload na API prod, volume no db prod | OK estático; reload real e isolamento de dados em runtime pendentes |
| pgAdmin | Extra: docker-compose.yml | GET /login na porta publicada e no container | OK: HTTP 200 |
| Comunicação pgAdmin-db | Extra: rede app e serviços db/pgadmin | Driver psycopg do pgAdmin executou SELECT 1 em db:5432 | OK; cadastro manual pela interface documentado, não executado |
| Saúde real | Extra: main.py | API local ligada ao PostgreSQL Docker; GET /health; stop db e novo GET | OK: 200/status ok e 503/mensagem genérica |
| Credenciais | .gitignore e .env.example | Inspeção e git check-ignore | Valores de demonstração; .env locais ignorados |
| Entrega | README.md e histórico Git | Branch feat/exercicios-docker; main contém somente preparação inicial | Commits separados com horários reais; sem push, merge ou PR |

## Limitação dos builds

Foram iniciados builds dos exercícios 1 e 2 pelo comando `up -d --build --wait`.
As imagens oficiais foram baixadas, mas a etapa `pip install` dentro do build
recebeu repetidamente **Network is unreachable** ao acessar o PyPI.
Os processos foram interrompidos após as tentativas, sem declarar sucesso.
Os comandos posteriores de build dev/prod/extra não chegaram a ser executados;
usam a mesma instalação de dependências e permanecem pendentes.

As dependências fixadas foram instaladas com sucesso em uma venv local, o que
permitiu executar os testes locais e compilar todos os módulos com compileall.
Isso não comprova o build das imagens Linux nem o funcionamento da API na porta
publicada por um container.

Para testar com banco real sem alterar o Compose entregue, foi usado um override
temporário com publicação em 127.0.0.1:15432, somente durante a validação.
Todas as APIs locais usaram esse banco de teste do extra; portanto esse teste
não comprova isolamento entre os bancos dev/prod. O override foi removido da
execução ao recriar os serviços com o Compose original. Os containers de teste
foram encerrados com down, preservando os volumes. Não foi usado down -v.
Nenhum recurso de outro projeto foi alterado.

## Pendências reais

1. Restabelecer acesso ao PyPI de dentro dos builds Docker e executar build/up
   dos cinco ambientes com os comandos de cada README.
2. Confirmar HTTP das APIs nas portas publicadas, criação/leitura e persistência
   por ambiente (exercícios 2, dev, prod e extra).
3. Confirmar reload ao editar código em dev e extra; ausência de alteração em
   prod; usuário sem root em runtime; bancos dev/prod simultâneos e isolados.
4. Cadastrar a conexão no pgAdmin pela interface e consultar a tabela tarefas.
5. Quando desejar entregar: criar/configurar remoto exercicios-orion, publicar
   a branch, abrir PR para main e solicitar revisão externa; enviar link ao mentor.

O título, a descrição sugerida do PR e cinco perguntas técnicas estão no README.
Não há aprovação simulada nem histórico retroativo entre 08/11 e 09/11.
