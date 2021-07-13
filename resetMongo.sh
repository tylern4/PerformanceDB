#!/usr/bin/env bash

# Bring containers down
docker compose down

# Remove volume with database storage
docker volume rm performancedb_performanceData