\set ON_ERROR_STOP on
BEGIN;
DO $$
BEGIN
  IF (SELECT count(*) FROM cursos) <> 3 OR (SELECT count(*) FROM alunos) <> 4 THEN
    RAISE EXCEPTION 'Quantidade incorreta de cursos/alunos';
  END IF;
  -- A exceção capturada cria um sub-bloco transacional sem dados residuais.
  BEGIN
    INSERT INTO alunos(id,nome,email,curso_id)
      VALUES (-1,'Inválido','invalido@example.com',-1);
    RAISE EXCEPTION 'A FK deveria ter rejeitado o curso inexistente';
  EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'OK: curso inexistente rejeitado pela FK';
  END;
END $$;
ROLLBACK;
SELECT * FROM alunos ORDER BY id;
