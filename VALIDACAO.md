# Verificações realizadas

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
