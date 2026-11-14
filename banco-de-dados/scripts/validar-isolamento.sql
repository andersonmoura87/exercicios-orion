\set ON_ERROR_STOP on
SELECT current_database() AS banco, current_user AS usuario;
DO $$
DECLARE outro text;
BEGIN
  outro := CASE current_database() WHEN 'orion_exercicios_dev' THEN 'orion_exercicios_prod'
             WHEN 'orion_exercicios_prod' THEN 'orion_exercicios_dev' END;
  IF outro IS NULL OR current_user <> current_database() THEN
    RAISE EXCEPTION 'Conexão fora dos bancos/usuários exclusivos';
  END IF;
  IF has_database_privilege(current_user, outro, 'CONNECT') OR
     EXISTS (SELECT 1 FROM pg_roles WHERE rolname=current_user
             AND (rolsuper OR rolcreatedb OR rolcreaterole OR rolreplication OR rolbypassrls)) THEN
    RAISE EXCEPTION 'Usuário tem privilégios além do ambiente';
  END IF;
END $$;
\echo OK: usuário limitado e sem CONNECT no outro ambiente
