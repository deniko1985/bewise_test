#!/usr/bin/env bash
docker exec -ti bewise_local alembic revision --autogenerate -m "Added required tables"
docker exec -ti bewise_local alembic upgrade head