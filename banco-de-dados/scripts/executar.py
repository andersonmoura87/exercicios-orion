"""Executa comandos SQL/mongosh e suas asserções, com autenticação e sem secrets em argv."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--existentes', choices=['dev', 'prod'], help='Usa docker exec nos containers do laboratório')
parser.add_argument('--etapa', choices=['1', '2', '3', '4', 'todos'], default='todos')
args = parser.parse_args()
env = os.environ.copy()
if args.existentes:
    arquivo = ROOT / f'.env.{args.existentes}'
    if not arquivo.exists():
        raise SystemExit('Execute primeiro scripts/provisionar.py')
    env.update(line.split('=', 1) for line in arquivo.read_text(encoding='utf-8').splitlines()
               if line and not line.startswith('#'))
for name in ('PGPASSWORD', 'MONGO_PASSWORD'):
    if env.get(name + '_FILE'):
        env[name] = Path(env[name + '_FILE']).read_text(encoding='utf-8').strip()
for name in ('PGDATABASE', 'PGUSER', 'PGPASSWORD', 'MONGO_DATABASE', 'MONGO_USER', 'MONGO_PASSWORD'):
    if not env.get(name) or env[name].startswith('SUBSTITUA_'):
        raise SystemExit(f'Configuração obrigatória ausente: {name}')
env.setdefault('PGHOST', 'postgres')
env.setdefault('PGPORT', '5432')
env['PGCLIENTENCODING'] = 'UTF8'
env.setdefault('MONGO_HOST', 'mongo')
env.setdefault('MONGO_PORT', '27017')

def executar(path, mongo=False):
    script = (ROOT / path).read_text(encoding='utf-8')
    if mongo:
        # authSource é o próprio banco do usuário limitado, nunca admin.
        script = ('db = db.getSiblingDB(process.env.MONGO_DATABASE);\n'
                  'if (!db.auth(process.env.MONGO_USER, process.env.MONGO_PASSWORD)) '
                  'throw new Error("Autenticação de exercício falhou");\n') + script
        cli = ['mongosh', '--quiet', '--host', env['MONGO_HOST'], '--port', env['MONGO_PORT'],
               '--file', '/dev/stdin']
    else:
        cli = ['psql', '-X', '-v', 'ON_ERROR_STOP=1', '-f', '-']
    if args.existentes:
        if mongo:
            cli[cli.index('--host') + 1] = '127.0.0.1'
        else:
            env['PGHOST'] = '127.0.0.1'
        variaveis = ['MONGO_DATABASE', 'MONGO_USER', 'MONGO_PASSWORD'] if mongo else [
            'PGDATABASE', 'PGUSER', 'PGPASSWORD', 'PGHOST', 'PGPORT']
        container = env.get('MONGO_CONTAINER', 'orion_mongo_db') if mongo else env.get('PG_CONTAINER', 'orion_postgres_db')
        cli = ['docker', 'exec', '-i', *[x for key in variaveis for x in ('-e', key)], container, *cli]
    print(f'>>> {path}', flush=True)
    result = subprocess.run(cli, input=script, text=True, encoding='utf-8', errors='replace', env=env, capture_output=True)
    # Sanitiza até erros inesperados de conexão; não exibe URIs com credenciais.
    for value in (result.stdout, result.stderr):
        for key in ('PGPASSWORD', 'MONGO_PASSWORD'):
            value = value.replace(env[key], '<redacted>')
        print(value, end='', flush=True)
    if result.returncode:
        raise SystemExit('Falha no script. Se o banco já existia, confira as credenciais reais; '
                         'mudar .env não altera usuários inicializados. Nenhum reset foi executado.')

if args.etapa in ('1', 'todos'):
    for file in ('01-schema.sql', '02-carga.sql', '03-verificar.sql'):
        executar('exercicio-1/' + file)
if args.etapa in ('2', 'todos'):
    executar('exercicio-2/01-consultas.sql')
if args.etapa in ('3', 'todos'):
    executar('exercicio-3/01-posts.js', mongo=True)
if args.etapa in ('4', 'todos'):
    executar('exercicio-4/01-consultas.js', mongo=True)
if args.etapa == 'todos':
    executar('scripts/validar-isolamento.sql')
    executar('scripts/validar-isolamento.js', mongo=True)
print('OK: execução e asserções concluídas')
