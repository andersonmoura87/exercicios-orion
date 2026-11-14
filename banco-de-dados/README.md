# Banco de dados

Laboratório de PostgreSQL e MongoDB: tabelas e carga em `exercicio-1/`, JOINs e
transferência em `exercicio-2/`, documentos flexíveis em `exercicio-3/`, comentários,
filtros e executor Docker em `exercicio-4/`. Não há API ou servidor HTTP.

Requer Docker Desktop (Linux), Compose v2 e Python 3.10+ no host, sem pacotes pip.
Esta entrega reutiliza `orion_postgres_db` (PostgreSQL 16) e `orion_mongo_db`, criados
pelo Compose externo `C:\Users\ander\bootcamp-db\docker-compose.yml`.
Em outro computador, provisione servidores autenticados equivalentes antes de executar.
O Compose externo e suas credenciais não fazem parte desta entrega.

## Ordem de execução (PowerShell, na raiz do repositório)

```powershell
docker start orion_postgres_db orion_mongo_db
python banco-de-dados/scripts/provisionar.py
python banco-de-dados/scripts/executar.py --existentes dev --etapa 1
python banco-de-dados/scripts/executar.py --existentes dev --etapa 2
python banco-de-dados/scripts/executar.py --existentes dev --etapa 3
python banco-de-dados/scripts/executar.py --existentes dev --etapa 4
```

O provisionamento usa os administradores existentes somente para criar bancos e
usuários `orion_exercicios_dev` e `orion_exercicios_prod`. Ele também conecta os
servidores a duas redes novas, preservando as conexões e os volumes anteriores.
Se os containers/admin PostgreSQL tiverem outros nomes, configure `PG_CONTAINER`,
`PG_ADMIN_USER`, `PG_ADMIN_DATABASE` e `MONGO_CONTAINER` no ambiente do processo.
O Mongo autentica o administrador em `admin`, usando o ambiente já existente no
container; o usuário dos exercícios autentica no próprio banco (`authSource`).

Secrets aleatórios são gerados em `banco-de-dados/secrets/`; `.env.dev` e `.env.prod`
também são locais e ignorados. `.env.example` contém apenas placeholders.
Dev usa arquivos de secrets; prod usa variáveis porque não pode ter mounts.
Secrets locais do Compose não são um cofre criptografado. Restrinja o acesso aos
arquivos com as permissões/ACL do sistema e não imprima `docker inspect` completo
ou `docker compose config` sem `--quiet` (podem mostrar secrets).

Se a autenticação falhar em banco já inicializado, interrompa e confira com o
responsável as credenciais reais e os arquivos locais. Não apague volumes, não
gere novos secrets por cima dos antigos e não presuma que editar `.env` altera
usuários existentes. O provisionador não troca senhas nem remove usuários.
Uma troca exige procedimento administrativo coordenado e atualização dos secrets.

## Dev, prod e validação

```powershell
$dev = 'banco-de-dados/exercicio-4/docker-compose.dev.yml'
$prod = 'banco-de-dados/exercicio-4/docker-compose.prod.yml'
docker compose --env-file banco-de-dados/.env.dev -f $dev config --quiet
docker compose --env-file banco-de-dados/.env.prod -f $prod config --quiet
docker compose --env-file banco-de-dados/.env.dev -f $dev build
docker compose --env-file banco-de-dados/.env.prod -f $prod build
docker compose --env-file banco-de-dados/.env.dev -f $dev up --abort-on-container-exit --exit-code-from exercicios
docker compose --env-file banco-de-dados/.env.prod -f $prod up --abort-on-container-exit --exit-code-from exercicios
python banco-de-dados/scripts/validar.py
```

O último comando executa os dois projetos simultaneamente, duas vezes, verifica
isolamento e mounts e grava saídas reais sanitizadas em `evidencias/`. Precisa das
duas imagens já construídas. Os executores são tarefas e terminam com código zero;
os bancos continuam ativos. Não é preciso reconstruir os bancos para repetir.
Para rodar só uma etapa via Compose: `docker compose --env-file ... -f ... run --rm exercicios --etapa 2`.
Para repetir todas sem build: `python banco-de-dados/scripts/executar.py --existentes dev`.
Os arquivos SQL/JS também podem ser executados diretamente em sessões autenticadas
de `psql`/`mongosh`, na ordem dos exercícios; o executor só fornece conexão e ordem.

Resultados: 3 cursos, 4 alunos, JOIN com 4 linhas, Maria (id 1) transferida para
Ciência de Dados (id 2), João permanece em Desenvolvimento Web e Redes de
Computadores não tem alunos. Mongo contém 2 posts: o primeiro sem `tags`, o segundo
com `['nosql','flexivel']` e um comentário de Ana, encontrado por campo aninhado.
As asserções falham com saída não zero; a FK inválida é capturada e revertida.

## Decisões e limites

- `text`, `NOT NULL`, PK e FK expressam os campos obrigatórios; não há unicidade de
  nome/email inventada. IDs de exemplo são estáveis e identities novas começam em
  100. A transferência usa IDs, consultas usam ordenação explícita.
- A DDL verifica estrutura e constraints existentes; carga SQL usa transação e
  compara conteúdo antes de concluir. Reexecução mantém a transferência de Maria:
  o estado anterior inicial só aparece na primeira execução em banco novo.
- Mongo usa `$setOnInsert` e `$addToSet`, sem validação rígida ou transações
  multidocumento. Dados incompatíveis geram erro; não há reset automático.
- Os projetos `orion-bd-dev` e `orion-bd-prod` têm redes, usuários e bancos distintos.
  Os servidores físicos são compartilhados: falhas/reinícios deles afetam ambos.
  Esse é isolamento lógico, não uma fronteira física contra administrador do Docker.
- Dev monta o código somente leitura. Prod contém apenas ferramentas cliente e
  scripts na imagem final, sem mounts, inclusive sem volumes anônimos herdados da
  imagem Mongo. O build copia somente `mongosh` da imagem oficial `mongo:8.0` para
  Ubuntu 24.04; não muda a versão dos servidores. Nenhuma imagem usa `latest`.
- “Sem montar volumes” aplica-se ao executor prod. Os bancos externos continuam
  persistentes nos volumes anteriores; não são bancos efêmeros nem servidores
  provisionados pelo Compose prod. Essa configuração é didática, não uma implantação
  de produção com gestão de secrets, backups, TLS e alta disponibilidade.
- As portas já expostas pelo Compose externo (5432/27017) foram preservadas; os
  executores não publicam portas nem precisam delas. O requisito de portas dev é
  atendido pela infraestrutura externa, sem duplicação. As publicações existentes
  não se restringem a loopback; corrigir isso exige uma alteração planejada nessa
  infraestrutura, fora desta entrega. Novas publicações devem usar `127.0.0.1`.
- `mongosh` em filesystem somente leitura emite aviso sobre `/.mongodb`; autenticação,
  consultas e verificações funcionam. Não foi liberada escrita nem montado tmpfs
  em prod apenas para remover esse aviso.

## Evidências e revisão

Consulte [VALIDACAO.md](VALIDACAO.md), `evidencias/dev.txt`, `evidencias/prod.txt` e
`evidencias/isolamento.txt`. Os PNGs são capturas reais desses logs no Bloco de notas,
não imagens geradas. Os quatro exercícios e o isolamento têm prints; nenhuma captura
está pendente. Se forem exigidos prints de execução interativa no terminal em vez
do visualizador de logs, execute os comandos acima e capture somente os resultados,
sem `.env`, comandos administrativos ou inspeções completas com credenciais.

O texto sugerido para PR está em [PR.md](PR.md). Não houve push, PR ou merge.
