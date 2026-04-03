# MiroFish Deployment Guide — GMKtec EVO-X2 / NucBox

**Target:** GMKtec EVO-X2 (128 GB RAM, ROCm) or NucBox  
**Date:** 2026-04-03  
**Deployed by:** Олег (@p314pm) with sudo access

---

## Prerequisites

### Hardware requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 32 GB | 64+ GB |
| CPU | 8 cores | 12+ cores |
| Storage | 100 GB SSD | 500 GB NVMe |
| GPU | Integrated | AMD ROCm capable |

### Software requirements

- Ubuntu 24.04 LTS (or WSL2 on Windows)
- Docker Desktop with Compose
- SSH access for remote deployment

---

## Deployment Steps

### Step 1: Clone MiroFish-Offline

```bash
# On GMKtec/NucBox
cd ~
git clone https://github.com/CarmiBanxe/MiroFish-Offline.git mirofish-engine
cd ~/mirofish-engine
```

### Step 2: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit configuration
nano .env
```

**Required settings in `.env`:**

```bash
# LLM Configuration (local Ollama)
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:32b
EMBEDDING_MODEL=nomic-embed-text

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<generate-strong-password>

# Application Settings
FLASK_PORT=3000
FLASK_HOST=0.0.0.0
DEBUG=false

# Banxe-specific (optional)
BANXE_SCENARIOS_PATH=/home/mmber/banxe-mirofish/scenarios
BANXE_REPORTS_PATH=/home/mmber/banxe-mirofish/reports
```

### Step 3: Start Docker Services

```bash
cd ~/mirofish-engine
docker compose up -d

# Verify services
docker compose ps
```

**Expected output:**
```
NAME                IMAGE                  STATUS
mirofish-neo4j      neo4j:5.15             Up
mirofish-ollama     ollama/ollama          Up
mirofish-app        mirofish-offline       Up
```

### Step 4: Pull Ollama Models

```bash
# Pull required models (may take 10-20 minutes)
ollama pull qwen2.5:32b
ollama pull nomic-embed-text

# Verify models
ollama list
```

### Step 5: Test API Health

```bash
# Local test
curl http://localhost:3000/api/health

# Expected response:
# {"status":"ok","agents":0,"simulations":0}

# Remote test (from another machine)
curl http://<gmktec-ip>:3000/api/health
```

### Step 6: Enable Remote Access (Optional)

For accessing MiroFish from other machines:

```bash
# Check firewall status
sudo ufw status

# Allow port 3000 if needed
sudo ufw allow 3000/tcp

# Or allow from specific IP only
sudo ufw allow from 192.168.0.0/24 to any port 3000 proto tcp
```

---

## Systemd Service (Auto-start on Boot)

Create systemd service for automatic startup:

```bash
sudo nano /etc/systemd/system/mirofish.service
```

**Service file content:**

```ini
[Unit]
Description=MiroFish Multi-Agent Simulation Engine
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/mmber/mirofish-engine
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=mmber
Group=mmber

[Install]
WantedBy=multi-user.target
```

**Enable service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable mirofish.service
sudo systemctl start mirofish.service
sudo systemctl status mirofish.service
```

---

## Performance Tuning

### For 128 GB RAM systems (GMKtec EVO-X2)

Edit `docker-compose.yml`:

```yaml
services:
  ollama:
    environment:
      - OLLAMA_NUM_PARALLEL=4
      - OLLAMA_MAX_LOADED_MODELS=2
    deploy:
      resources:
        reservations:
          memory: 64G
  
  neo4j:
    environment:
      - NEO4J_dbms_memory_heap_initial__size=16g
      - NEO4J_dbms_memory_heap_max__size=32g
```

### For systems with AMD GPU (ROCm)

```yaml
services:
  ollama:
    devices:
      - /dev/kfd:/dev/kfd
      - /dev/dri:/dev/dri
    environment:
      - HSA_OVERRIDE_GFX_VERSION=11.0.0
```

---

## Monitoring

### Check service health

```bash
# Docker containers
docker compose ps

# Resource usage
docker stats

# Logs
docker compose logs -f mirofish-app
docker compose logs -f ollama
docker compose logs -f neo4j
```

### Neo4j Browser

Access Neo4j browser at: http://<gmktec-ip>:7474

**Credentials:**
- Username: `neo4j`
- Password: (from `.env`)

### Ollama API

```bash
# List loaded models
curl http://localhost:11434/api/tags

# Test model
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:32b",
  "prompt": "Hello",
  "stream": false
}'
```

---

## Backup & Recovery

### Backup Neo4j data

```bash
# Stop MiroFish
cd ~/mirofish-engine
docker compose down

# Backup Neo4j data directory
tar -czf neo4j-backup-$(date +%Y%m%d).tar.gz \
    ~/.local/share/mirofish-engine/neo4j/data

# Restart
docker compose up -d
```

### Restore from backup

```bash
docker compose down
tar -xzf neo4j-backup-YYYYMMDD.tar.gz -C ~/
docker compose up -d
```

---

## Troubleshooting

### Problem: OOM (Out of Memory)

**Symptoms:** Containers killed unexpectedly

**Solution:**
```bash
# Reduce model size or parallelism
nano docker-compose.yml
# Lower OLLAMA_NUM_PARALLEL and memory limits

# Or add swap
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Problem: GPU not detected

**Symptoms:** Slow inference, CPU-only mode

**Check:**
```bash
# Verify ROCm installation
rocm-smi

# Check Ollama device access
ls -la /dev/kfd /dev/dri
```

**Solution:**
```bash
# Add user to render group
sudo usermod -aG render $USER

# Reboot required
sudo reboot
```

### Problem: Port conflicts

**Symptoms:** "Address already in use" error

**Check:**
```bash
sudo netstat -tlnp | grep :3000
sudo netstat -tlnp | grep :7687
```

**Solution:** Change ports in `.env` and `docker-compose.yml`

---

## Security Hardening

### Firewall rules

```bash
# Allow only necessary ports
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 3000/tcp  # MiroFish API
sudo ufw allow 7474/tcp # Neo4j Browser (optional)
sudo ufw enable
```

### Neo4j authentication

```bash
# Change default password immediately
docker compose exec neo4j neo4j-admin set-initial-password <new-password>
```

### HTTPS (Optional)

For production deployments, add reverse proxy:

```bash
# Install nginx
sudo apt install nginx

# Configure SSL with Let's Encrypt
sudo certbot --nginx -d mirofish.banxe.com
```

---

## Verification Checklist

- [ ] Docker Compose services running
- [ ] Ollama models pulled (qwen2.5:32b, nomic-embed-text)
- [ ] API health check passes
- [ ] Neo4j browser accessible
- [ ] Systemd service enabled
- [ ] Firewall configured
- [ ] Backup procedure tested

---

## Contact

| Person | Role | Access |
|--------|------|--------|
| Олег | CTIO Deputy | sudo NOPASSWD on GMKtec |
| Moriel Carmi | CEO/CTIO | Full access |

---

## Related Documentation

- `MIROFISH-INTEGRATION.md` — Full integration plan
- `MIROFISH-GITHUB-SETUP.md` — GitHub repository setup
- `~/mirofish-engine/README.md` — Engine documentation
