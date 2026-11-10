# Exercício 1

Execute em PowerShell, a partir da raiz do repositório:

```powershell
Set-Location docker/exercicio-1
docker compose config --quiet
docker compose build
docker compose up -d --wait
docker compose logs -f api # Ctrl+C encerra a visualização dos logs
```

API: http://localhost:3000. Swagger: http://localhost:3000/docs.
As portas são publicadas apenas em 127.0.0.1.

```powershell
curl.exe -sS http://localhost:3000/
```

Resposta exata: `Hello from Docker!` (texto simples).

## Encerramento

```powershell
docker compose down
# DESTRUTIVO: remove os volumes e todos os dados deste projeto.
docker compose down -v
```

A imagem oficial Python slim usa Debian reduzido e permite instalar wheels sem
compiladores adicionais. As dependências diretas são fixadas em requirements.txt.
Copiar requirements.txt antes do código permite reutilizar o cache de instalação.
`.dockerignore` exclui arquivos locais do contexto de build. O usuário sem root
reduz os privilégios da API. Não há importações dos outros exercícios.
