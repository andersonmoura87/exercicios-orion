\set ON_ERROR_STOP on
BEGIN;
SELECT a.nome, c.nome_curso FROM alunos a
INNER JOIN cursos c ON c.id = a.curso_id ORDER BY a.id;

SELECT a.nome, c.nome_curso FROM alunos a
JOIN cursos c ON c.id = a.curso_id
WHERE c.nome_curso = 'Desenvolvimento Web' ORDER BY a.id;

\echo Maria antes da transferência (em reexecuções, já estará em Ciência de Dados)
SELECT a.id, a.nome, c.nome_curso FROM alunos a
JOIN cursos c ON c.id = a.curso_id WHERE a.id = 1 ORDER BY a.id;

UPDATE alunos SET curso_id = 2 WHERE id = 1;

\echo Maria depois da transferência
SELECT a.id, a.nome, c.nome_curso FROM alunos a
JOIN cursos c ON c.id = a.curso_id WHERE a.id = 1 ORDER BY a.id;

SELECT c.id, c.nome_curso FROM cursos c
LEFT JOIN alunos a ON a.curso_id = c.id WHERE a.id IS NULL ORDER BY c.id;

DO $$
BEGIN
  IF (SELECT curso_id FROM alunos WHERE id=1) IS DISTINCT FROM 2 OR
     (SELECT count(*) FROM alunos a JOIN cursos c ON c.id=a.curso_id) <> 4 OR
     (SELECT array_agg(a.id ORDER BY a.id) FROM alunos a JOIN cursos c ON c.id=a.curso_id
       WHERE c.nome_curso='Desenvolvimento Web') IS DISTINCT FROM ARRAY[2] OR
     (SELECT array_agg(c.id ORDER BY c.id) FROM cursos c LEFT JOIN alunos a ON a.curso_id=c.id
       WHERE a.id IS NULL) IS DISTINCT FROM ARRAY[3] THEN
    RAISE EXCEPTION 'Falha na transferência, JOIN, filtro ou curso sem alunos';
  END IF;
END $$;
COMMIT;
