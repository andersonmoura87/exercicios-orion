# Validação real — 13/11/2026 (America/Sao_Paulo)

Clone confirmado por `git remote -v`:
`https://github.com/andersonmoura87/exercicios-orion.git`, no clone local de publicação existente.
Não havia AGENTS.md aplicável ou configuração Gitflow. Working tree inicial limpa.
A feature foi criada da main local `165e55b`, conforme solicitado; após fetch,
`origin/main` estava em `61a3c5e`, 8 commits à frente. Esses commits pertencem à
entrega Docker já incorporada remotamente. Na revisão final, foi executado novo
fetch e a divergência era de 8 commits de cada lado. `origin/main` foi integrada
à feature pelo merge `fe6d534`, sem conflitos e sem alterar a main local `165e55b`.
Os 8 commits anteriores foram preservados; não houve rebase nem reescrita.
O diff final contra `origin/main` contém apenas `banco-de-dados/`.

| Verificação executada | Resultado |
|---|---|
| PostgreSQL real com psql, usuário do exercício | Schema, 3 cursos, 4 alunos, SELECT e FK inválida isolada aprovados |
| JOIN, WHERE, UPDATE por ID e LEFT JOIN | Maria de Web para Ciência de Dados; curso 3 sem alunos |
| MongoDB real com mongosh autenticado | Dois posts, ausência de tags no primeiro e array exato no segundo |
| Comentário, filtro por tag/autor/campo aninhado | Um comentário; filtros aprovados; repetição sem duplicação |
| Reexecução completa | Dev e prod simultâneos, duas rodadas com exit 0 |
| Permissões | Papel PostgreSQL sem privilégios administrativos/CONNECT cruzado; leitura Mongo cruzada rejeitada com código 13 |
| Compose config --quiet | Dev e prod válidos |
| Builds e execução real | Targets desenvolvimento e final construídos e executados |
| Runtime | UID 10001, filesystem somente leitura, redes distintas, dev com 3 mounts e prod com 0 |
| Bancos existentes | Containers apenas iniciados/conectados às redes novas; mounts e volumes preservados |
| Secrets | Arquivos locais ignorados; stage conferido contra secrets locais e dos containers, sem exibir valores |

As saídas completas de duas rodadas estão em `evidencias/dev.txt` e
`evidencias/prod.txt`; `isolamento.txt` registra inspeções verificadas. Somente
sequências ANSI, espaços finais e secrets são sanitizados pelo gravador de logs.
Os logs dev/prod foram renovados depois do merge: duas rodadas simultâneas
com exit 0 e as mesmas asserções de conteúdo, constraints, permissões e mounts.
O log histórico `evidencias/prod-inicial.txt` preserva Maria antes/depois da primeira
transferência; as novas rodadas já começam com Maria em Ciência de Dados.
A reexecução não desfaz a transferência. Não foi necessário novo build: a integração
não modificou Dockerfile, Compose, executor ou scripts SQL/JS do laboratório.

Capturas reais no visualizador desses logs: `exercicio-1.png` (carga),
`exercicio-2.png` (FK, JOINs, antes/depois e curso sem alunos), `exercicio-3.png`
(documentos com/sem tags), `exercicio-4.png` (tags e comentários) e `isolamento.png`.
Não houve fabricação de resultados. Prints de terminal interativo podem ser feitos
opcionalmente conforme o README se o avaliador exigir esse formato específico.

Limites: servidores compartilhados, portas externas originais preservadas, prod sem
mounts apenas no executor. Há aviso de log do mongosh no filesystem somente leitura.
O Compose externo contém credenciais fixas e mongo:latest; não foi versionado,
alterado nem usado como modelo de segurança. Nenhuma credencial foi rotacionada.
As verificações de schema, conteúdo e isolamento não são auditoria de segurança
completa. Nenhum volume, banco preexistente ou container de outro exercício foi removido.

## Revisão antes da publicação

Revisados todos os arquivos do diff contra origin/main, os logs e os cinco PNGs.
Os prints foram recapturados em janela separada, sem títulos de abas alheias;
exercícios 1–4 exibem o log inicial preservado, e isolamento exibe a nova validação.
Caminhos pessoais desnecessários foram removidos dos guias. Os nomes e e-mails
dos dados de exemplo são fictícios, com domínio example.com. A auditoria comparou
os arquivos com os secrets locais e dos containers e procurou tokens, chaves
privadas e URIs com credenciais, sem reproduzir os valores. Nenhum secret completo
foi encontrado nos arquivos finais; as verificações por padrões não são garantia
absoluta. As capturas anteriores continuam no histórico, que não foi reescrito.
git diff --check e a revisão do stage precederam os novos commits.
Sem push, abertura de PR ou merge na main. Revisão externa permanece pendente.
