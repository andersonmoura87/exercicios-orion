const resultado = db.posts.updateOne({_id: 'post-2'}, {$addToSet: {
  comentarios: {autor: 'Ana', texto: 'Bom exemplo de documento flexível.'}
}});
if (resultado.matchedCount !== 1) throw new Error('Execute primeiro o exercício 3');
print('Posts com tag nosql');
printjson(db.posts.find({tags: 'nosql'}).sort({_id: 1}).toArray());
print('Posts de Maria');
printjson(db.posts.find({autor: 'Maria'}).sort({_id: 1}).toArray());
print('Posts com comentário de Ana');
printjson(db.posts.find({'comentarios.autor': 'Ana'}).sort({_id: 1}).toArray());
const ids = filtro => db.posts.find(filtro).sort({_id: 1}).toArray().map(p => p._id);
if (JSON.stringify(ids({tags: 'nosql'})) !== '["post-2"]' ||
    JSON.stringify(ids({autor: 'Maria'})) !== '["post-1"]' ||
    JSON.stringify(ids({'comentarios.autor': 'Ana'})) !== '["post-2"]' ||
    JSON.stringify(db.posts.findOne({_id: 'post-2'}).comentarios) !==
      JSON.stringify([{autor: 'Ana', texto: 'Bom exemplo de documento flexível.'}])) {
  throw new Error('Falha nos filtros ou comentário duplicado/incompatível');
}
print('OK: tags, autor e comentário aninhado; sem duplicação');
