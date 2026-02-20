# Container Dead Monitor

A minimalistic Docker container that monitors the health of another container and sends an alert to a Discord Webhook if it goes down. 
Built using Python 3.13 on Alpine Linux and dependency resolution via `uv` for maximum compactness and speed.

## Quick Start

1. Duplicate `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in `.env` with your Discord webhook URL and the name of the container you want to monitor.

3. Run the monitor via Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

## Requirements

Ensure `/var/run/docker.sock` is mounted into the container so it can communicate with your host's Docker daemon.