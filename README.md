## 📁 Complete Project Setup

### 1. First, let's create the complete directory structure:

```bash
# Navigate to your Polis directory
cd ~/Downloads/Polis

# Remove any existing files and create fresh structure
rm -rf *
mkdir -p {backend,frontend,shared}

# Create all required files
touch docker-compose.yml Dockerfile.backend Dockerfile.frontend
touch backend/main.py backend/requirements.txt
touch frontend/app.py frontend/requirements.txt
touch shared/__init__.py shared/models.py
```

#### `shared/__init__.py`
```python
# This file makes the shared directory a Python package
```

### 2. Now build and run:

```bash
# Make sure you're in the Polis directory
cd ~/Downloads/Polis

# Build and start the services
docker-compose up --build
```

### 3. Verify the services are running:

Open two new terminals and test:

**Terminal 1 - Test backend:**
```bash
curl http://localhost:8000/api/health
```

**Terminal 2 - Check logs:**
```bash
docker-compose logs -f
```

### 4. Access your application:

- **Frontend Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
