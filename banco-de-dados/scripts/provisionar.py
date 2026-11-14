"""Provisiona bancos exclusivos nos containers existentes; não altera senhas existentes."""
import json
import os
from pathlib import Path
import secrets
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def docker(container, args, script):
    result = subprocess.run(['docker', 'exec', '-i', container, *args],
                            input=script, text=True, encoding='utf-8', capture_output=True)
    if result.returncode:
        # Saídas de provisionamento podem conter comandos com secrets.
        raise SystemExit(f'Falha de provisionamento em {container}; verifique autenticação, '
                         'propriedade dos bancos e credenciais já inicializadas. Nada foi apagado. '
                         'Não mude apenas o .env para tentar trocar senhas.')

def sql_literal(value):
    return "'" + value.replace("'", "''") + "'"

for ambiente in ('dev', 'prod'):
    banco = f'orion_exercicios_{ambiente}'
    usuario = f'orion_exercicios_{ambiente}'
    config = ROOT / f'.env.{ambiente}'
    pasta = ROOT / 'secrets'
    pasta.mkdir(exist_ok=True)
    pg_file = pasta / f'{ambiente}.pg'
    mongo_file = pasta / f'{ambiente}.mongo'
    for arquivo in (pg_file, mongo_file):
        if not arquivo.exists():
            with arquivo.open('x', encoding='utf-8') as stream:
                stream.write(secrets.token_urlsafe(32))
            os.chmod(arquivo, 0o600)
    pg_pass = pg_file.read_text(encoding='utf-8')
    mongo_pass = mongo_file.read_text(encoding='utf-8')
    # Arquivos locais ignorados; prod usa env porque a exigência exclui mounts.
    if not config.exists():
        config.write_text(f'PGDATABASE={banco}\nPGUSER={usuario}\n'
                          f'MONGO_DATABASE={banco}\nMONGO_USER={usuario}\n'
                          f'PGPASSWORD={pg_pass}\nMONGO_PASSWORD={mongo_pass}\n', encoding='utf-8')
        os.chmod(config, 0o600)
    docker(os.environ.get('PG_CONTAINER', 'orion_postgres_db'),
           ['psql', '-X', '-v', 'ON_ERROR_STOP=1', '-U',
            os.environ.get('PG_ADMIN_USER', 'orion_user'), '-d',
            os.environ.get('PG_ADMIN_DATABASE', 'orion_db')],
           f"SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', {sql_literal(usuario)}, "
           f"{sql_literal(pg_pass)}) WHERE NOT EXISTS "
           f"(SELECT FROM pg_roles WHERE rolname={sql_literal(usuario)}) \\gexec\n"
           f"SELECT format('CREATE DATABASE %I OWNER %I', {sql_literal(banco)}, "
           f"{sql_literal(usuario)}) WHERE NOT EXISTS "
           f"(SELECT FROM pg_database WHERE datname={sql_literal(banco)}) \\gexec\n"
           f"DO $$ BEGIN IF (SELECT pg_get_userbyid(datdba) FROM pg_database "
           f"WHERE datname={sql_literal(banco)}) IS DISTINCT FROM {sql_literal(usuario)} "
           f"THEN RAISE EXCEPTION 'Banco pertence a outro usuario'; END IF; END $$;\n"
           f"REVOKE CONNECT, TEMPORARY ON DATABASE {banco} FROM PUBLIC;\n")
    docker(os.environ.get('MONGO_CONTAINER', 'orion_mongo_db'), ['mongosh', '--quiet', '--file', '/dev/stdin'],
           'const admin = db.getSiblingDB("admin");\n'
           'if (!admin.auth(process.env.MONGO_INITDB_ROOT_USERNAME, '
           'process.env.MONGO_INITDB_ROOT_PASSWORD)) throw new Error("Admin auth falhou");\n'
           f'const lab = db.getSiblingDB({json.dumps(banco)});\n'
           f'if (!lab.getUser({json.dumps(usuario)})) lab.createUser('
           + json.dumps({'user': usuario, 'pwd': mongo_pass,
                         'roles': [{'role': 'readWrite', 'db': banco}]}) + ');\n')
    print(f'Provisionamento solicitado: {ambiente}; valide autenticação com o executor.')
