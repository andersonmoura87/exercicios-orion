// IDs reservados tornam a carga repetível sem substituir documentos existentes.
if (!db.getCollectionNames().includes('posts')) db.createCollection('posts');
db.posts.updateOne({_id: 'post-1'}, {$setOnInsert: {
  titulo: 'Primeiro post', autor: 'Maria', conteudo: 'Um documento sem tags.'
}}, {upsert: true});
db.posts.updateOne({_id: 'post-2'}, {$setOnInsert: {
  titulo: 'Schema flexível', autor: 'João', conteudo: 'Campos podem variar.',
  tags: ['nosql', 'flexivel']
}}, {upsert: true});
printjson(db.posts.find().sort({_id: 1}).toArray());
const primeiro = db.posts.findOne({_id: 'post-1'});
const segundo = db.posts.findOne({_id: 'post-2'});
if (db.posts.countDocuments({}) !== 2 ||
    Object.hasOwn(primeiro, 'tags') ||
    JSON.stringify(segundo.tags) !== JSON.stringify(['nosql', 'flexivel']) ||
    primeiro.titulo !== 'Primeiro post' || primeiro.autor !== 'Maria' ||
    primeiro.conteudo !== 'Um documento sem tags.' ||
    segundo.titulo !== 'Schema flexível' || segundo.autor !== 'João' ||
    segundo.conteudo !== 'Campos podem variar.') {
  throw new Error('Documentos incompatíveis com a carga esperada');
}
print('OK: dois documentos, primeiro sem tags e segundo com array esperado');
