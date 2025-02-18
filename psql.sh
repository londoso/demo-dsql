# conexión mediante cloudshell
export PGPASSWORD=$(aws dsql generate-db-connect-admin-auth-token --expires-in 3600 --region us-east-1 --hostname siabt3etsijuyijmtlu2nw6scy.dsql.us-east-1.on.aws)

PGSSLMODE=require

psql --dbname postgres --username admin --host siabt3etsijuyijmtlu2nw6scy.dsql.us-east-1.on.aws