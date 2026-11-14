# Título

feat(db): implementa exercícios de PostgreSQL e MongoDB com execução Docker

# Destino

`main` — origem: `feat/exercicios-banco-de-dados`.

# Descrição

Adiciona o laboratório em banco-de-dados/: tabelas cursos/alunos com PK/FK e carga
fictícia, JOINs e transferência de Maria por ID, posts MongoDB com schema flexível,
comentários e consultas por tags, autor e campo aninhado. Scripts incluem asserções
e reexecução sem duplicação ou reset de dados.

Reutiliza os containers externos do laboratório, com usuários/bancos e redes
distintos para dev/prod. O executor dev monta o código; a imagem final prod contém
os scripts e executa sem mounts. Não adiciona servidores de banco, API ou frontend.
Inclui provisionamento sem troca de senhas, secrets locais ignorados e documentação.

Validação: psql e mongosh reais; constraints, carga, JOINs, transferência, curso sem
alunos, arrays e comentários; dois projetos simultâneos em duas rodadas com exit 0;
acesso cruzado negado; Compose válidos; builds concluídos; prod com zero mounts e
volumes existentes preservados. Evidências textuais e prints em banco-de-dados/evidencias/.

Limites para revisão: isolamento lógico em servidores compartilhados; portas
externas originais mantidas; sem mounts refere-se ao executor prod. Não é uma stack
de produção real. O aviso de log do mongosh não interfere nas consultas.

Base atualizada: origin/main (61a3c5e) integrada à feature pelo merge fe6d534,
sem conflitos e preservando os 8 commits anteriores. A main local não foi alterada.
O diff contra origin/main está restrito a banco-de-dados/. Após a integração,
dev/prod passaram novamente em duas rodadas simultâneas; logs foram renovados e
o log inicial foi preservado separadamente para mostrar a transferência original.
Os cinco prints foram revisados e recapturados sem abas alheias. Guias, logs e
arquivos finais passaram pela busca de secrets e URIs com credenciais.
Sem prints obrigatórios pendentes; revisão externa e publicação ficam para a
próxima etapa autorizada. Nenhum push, abertura de PR ou merge na main.
