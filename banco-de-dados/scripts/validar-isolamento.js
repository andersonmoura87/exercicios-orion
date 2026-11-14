const outroBanco = db.getName() === 'orion_exercicios_dev' ? 'orion_exercicios_prod' :
                   db.getName() === 'orion_exercicios_prod' ? 'orion_exercicios_dev' : null;
if (!outroBanco) throw new Error('Banco não pertence aos ambientes exclusivos');
let negada = false;
try {
  db.getSiblingDB(outroBanco).runCommand({count: 'posts', query: {}});
} catch (erro) {
  if (erro.code !== 13) throw erro;
  negada = true;
}
if (!negada) throw new Error('Leitura no outro ambiente deveria ser Unauthorized');
print('OK: leitura cruzada MongoDB rejeitada (Unauthorized 13)');
