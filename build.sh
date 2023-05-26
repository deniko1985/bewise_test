#!/usr/bin/env bash
mkdir -p src/audio_files/mp3 src/audio_files/wav
mv ./src/.env_example ./src/.env
docker-compose up --build -d
docker exec -ti postgres_bewise_local psql -U postgres -p 5444 <<-EOSQL
CREATE DATABASE bewise_test;
EOSQL
docker restart bewise_local
bash ./run_migration.sh