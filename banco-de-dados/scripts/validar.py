"""Validação real dos dois projetos Compose; requer build e provisionamento prévios."""
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
evidencias = ROOT / 'evidencias'
evidencias.mkdir(exist_ok=True)
containers = [os.environ.get('PG_CONTAINER', 'orion_postgres_db'),
              os.environ.get('MONGO_CONTAINER', 'orion_mongo_db')]

def inspect(nomes):
    return json.loads(subprocess.check_output(['docker', 'inspect', *nomes]))

mounts_antes = {c['Name']: c['Mounts'] for c in inspect(containers)}
secrets = [p.read_text(encoding='utf-8').strip() for p in (ROOT / 'secrets').iterdir() if p.is_file()]
logs = {a: [] for a in ('dev', 'prod')}
for rodada in (1, 2):
    processos = {}
    for ambiente in ('dev', 'prod'):
        cmd = ['docker', 'compose', '--env-file', str(ROOT / f'.env.{ambiente}'),
               '-f', str(ROOT / 'exercicio-4' / f'docker-compose.{ambiente}.yml')]
        subprocess.run([*cmd, 'config', '--quiet'], check=True)
        processos[ambiente] = subprocess.Popen(
            [*cmd, 'up', '--no-build', '--abort-on-container-exit', '--exit-code-from', 'exercicios'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for ambiente, processo in processos.items():
        saida = processo.communicate()[0].decode('utf-8', errors='replace')
        saida = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', saida)
        saida = '\n'.join(line.rstrip() for line in saida.splitlines()) + '\n'
        for secret in secrets:
            saida = saida.replace(secret, '<redacted>')
        logs[ambiente].append(f'RODADA {rodada}\n' + saida)
        (evidencias / f'{ambiente}.txt').write_text('\n'.join(logs[ambiente]), encoding='utf-8')
        if processo.returncode or 'OK: execução e asserções concluídas' not in saida:
            raise SystemExit(f'Falha em {ambiente}: consulte evidencias/{ambiente}.txt')
        print(f'OK: {ambiente}, rodada {rodada}, código zero')

resumo = []
for ambiente in ('dev', 'prod'):
    c = inspect([f'orion-bd-{ambiente}-exercicios-1'])[0]
    assert c['State']['ExitCode'] == 0
    assert c['Config']['User'] == '10001:10001'
    assert c['HostConfig']['ReadonlyRootfs']
    assert set(c['NetworkSettings']['Networks']) == {f'orion-bd-{ambiente}_executor'}
    assert not c['HostConfig']['PortBindings']
    if ambiente == 'prod':
        assert not c['Mounts'], 'Prod não pode ter nenhum mount, nem volumes anônimos'
    else:
        assert any(m['Destination'] == '/lab' and not m['RW'] for m in c['Mounts'])
    resumo.append(f'{ambiente}: exit=0; UID=10001; rede exclusiva; '
                  f'mounts={len(c["Mounts"])}; nenhuma porta nova publicada')
assert mounts_antes == {c['Name']: c['Mounts'] for c in inspect(containers)}
resumo.append('Volumes e mounts dos bancos existentes preservados durante a validação.')
(evidencias / 'isolamento.txt').write_text('\n'.join(resumo) + '\n', encoding='utf-8')
print('\n'.join(resumo))
