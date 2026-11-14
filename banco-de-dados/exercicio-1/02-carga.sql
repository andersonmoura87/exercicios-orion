\set ON_ERROR_STOP on
BEGIN;
INSERT INTO cursos (id, nome_curso) VALUES
  (1, 'Desenvolvimento Web'), (2, 'Ciência de Dados'), (3, 'Redes de Computadores')
ON CONFLICT (id) DO NOTHING;
INSERT INTO alunos (id, nome, email, curso_id) VALUES
  (1, 'Maria', 'maria@example.com', 1),
  (2, 'João', 'joao@example.com', 1),
  (3, 'Ana', 'ana@example.com', 2),
  (4, 'Pedro', 'pedro@example.com', 2)
ON CONFLICT (id) DO NOTHING;
-- Não sobrescreve alterações existentes nem desfaz a transferência de Maria.
DO $$
BEGIN
  IF (SELECT count(*) FROM cursos) <> 3 OR (SELECT count(*) FROM alunos) <> 4 OR
     EXISTS (SELECT 1 FROM (VALUES (1,'Desenvolvimento Web'),(2,'Ciência de Dados'),
       (3,'Redes de Computadores')) AS e(id,nome)
       LEFT JOIN cursos c USING(id) WHERE c.nome_curso IS DISTINCT FROM e.nome) OR
     EXISTS (SELECT 1 FROM (VALUES (1,'Maria','maria@example.com'),
       (2,'João','joao@example.com'),(3,'Ana','ana@example.com'),
       (4,'Pedro','pedro@example.com')) AS e(id,nome,email)
       LEFT JOIN alunos a USING(id)
       WHERE a.nome IS DISTINCT FROM e.nome OR a.email IS DISTINCT FROM e.email) OR
     EXISTS (SELECT 1 FROM alunos WHERE
       (id=1 AND curso_id NOT IN (1,2)) OR (id=2 AND curso_id<>1) OR
       (id IN (3,4) AND curso_id<>2)) THEN
    RAISE EXCEPTION 'Carga incompatível: esperado banco exclusivo do laboratório';
  END IF;
END $$;
COMMIT;
SELECT * FROM alunos ORDER BY id;
