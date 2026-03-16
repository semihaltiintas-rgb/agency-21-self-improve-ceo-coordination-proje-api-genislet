# CEO Çıktısı

# Proje Geliştirme Planı: API Genişletme & Dashboard

## 1. Proje Özeti

Mevcut AI ajan sistemine `status`, `phase`, `agent_outputs`, `quality_score`, `cost` alanları eklenerek API genişletilecektir. Bu genişleme için SQLite veritabanı migration'ı yapılacak, FastAPI backend endpoint'leri güncellenecek ve React dashboard'u yeni verilerle zenginleştirilecektir. Proje, CEO koordinasyonunda 3 paralel modül olarak yürütülecektir.

---

## 2. Modüller

### 📦 MODÜL 1: Database Migration
| Alan | Detay |
|------|-------|
| **Ad** | DB Schema Extension |
| **Sorumlu Ajan** | DB Agent (Agent-3) |
| **Öncelik** | 🔴 KRİTİK - İlk yapılacak |
| **Bağımlılık** | Yok - Başlangıç noktası |

**Görevler:**
```sql
-- projects tablosuna eklenecek alanlar:
ALTER TABLE projects ADD COLUMN status TEXT DEFAULT 'pending';
-- ['pending', 'running', 'completed', 'failed', 'paused']

ALTER TABLE projects ADD COLUMN phase TEXT DEFAULT 'init';
-- ['init', 'planning', 'execution', 'review', 'done']

ALTER TABLE projects ADD COLUMN agent_outputs TEXT DEFAULT '{}';
-- JSON blob: {agent_id: output_text}

ALTER TABLE projects ADD COLUMN quality_score REAL DEFAULT 0.0;
-- 0.0 - 100.0 arası float

ALTER TABLE projects ADD COLUMN cost REAL DEFAULT 0.0;
-- USD cinsinden float
```

**Migration Stratejisi:**
```python
# migration_v2.py
import sqlite3, json
from datetime import datetime

MIGRATION_SCRIPT = """
BEGIN TRANSACTION;
  ALTER TABLE projects ADD COLUMN status TEXT DEFAULT 'pending';
  ALTER TABLE projects ADD COLUMN phase TEXT DEFAULT 'init';
  ALTER TABLE projects ADD COLUMN agent_outputs TEXT DEFAULT '{}';
  ALTER TABLE projects ADD COLUMN quality_score REAL DEFAULT 0.0;
  ALTER TABLE projects ADD COLUMN cost REAL DEFAULT 0.0;
  
  CREATE TABLE IF NOT EXISTS migration_history (
    id INTEGER PRIMARY KEY,
    version TEXT,
    applied_at TIMESTAMP,
    description TEXT
  );
  
  INSERT INTO migration_history VALUES 
    (NULL, 'v2.0', datetime('now'), 'API fields extension');
COMMIT;
"""
```

---

### 📦 MODÜL 2: Backend API Genişletme
| Alan | Detay |
|------|-------|
| **Ad** | FastAPI Extension |
| **Sorumlu Ajan** | Backend Agent (Agent-1) |
| **Öncelik** | 🔴 KRİTİK - Modül 1 sonrası |
| **Bağımlılık** | Modül 1 tamamlanmalı |

**Görevler:**

```python
# ---- PYDANTIC MODELS ----
from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

class ProjectStatus(str, Enum):
    PENDING   = "pending"
    RUNNING   = "running"
    COMPLETED = "completed"
    FAILED    = "failed"
    PAUSED    = "paused"

class ProjectPhase(str, Enum):
    INIT      = "init"
    PLANNING  = "planning"
    EXECUTION = "execution"
    REVIEW    = "review"
    DONE      = "done"

class ProjectResponse(BaseModel):
    id:            int
    name:          str
    description:   Optional[str]
    status:        ProjectStatus
    phase:         ProjectPhase
    agent_outputs: Dict[str, Any]
    quality_score: float          # 0.0 - 100.0
    cost:          float          # USD
    created_at:    str
    updated_at:    Optional[str]

class ProjectUpdateRequest(BaseModel):
    status:        Optional[ProjectStatus]
    phase:         Optional[ProjectPhase]
    agent_outputs: Optional[Dict[str, Any]]
    quality_score: Optional[float]
    cost:          Optional[float]
```

**Yeni/Güncellenen Endpoint'ler:**

```python
# GET /api/projects → Tüm yeni alanlarla döner
@app.get("/api/projects", response_model=List[ProjectResponse])
async def get_projects():
    ...

# GET /api/projects/{id} → Detay + agent_outputs
@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    ...

# PATCH /api/projects/{id} → Kısmi güncelleme
@app.patch("/api/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, data: ProjectUpdateRequest):
    ...

# GET /api/projects/{id}/agent-outputs → Sadece ajan çıktıları
@app.get("/api/projects/{project_id}/agent-outputs")
async def get_agent_outputs(project_id: int):
    ...

# POST /api/run → Çalıştırırken status/phase güncelle
@app.post("/api/run")
async def run_project(request: RunRequest):
    # status: pending → running
    # phase: init → execution
    # Her ajan tamamlandıkça agent_outputs güncelle
    # Bitince quality_score hesapla, cost ekle
    ...

# GET /api/projects/stats/summary → Dashboard için aggregate
@app.get("/api/projects/stats/summary")
async def get_stats_summary():
    return {
        "total_cost":     float,
        "avg_quality":    float,
        "by_status":      dict,
        "by_phase":       dict,
        "agent_activity": dict
    }
```

**Ajan Output Güncelleme Mekanizması:**
```python
async def update_agent_output(project_id: int, agent_id: str, output: str):
    """Her ajan tamamlandığında çağrılır"""
    project = db.get(project_id)
    outputs = json.loads(project.agent_outputs)
    outputs[agent_id] = {
        "output":       output,
        "completed_at": datetime.now().isoformat(),
        "tokens_used":  calculate_tokens(output)
    }
    cost = calculate_cost(outputs)  # Token bazlı maliyet
    db.update(project_id, 
              agent_outputs=json.dumps(outputs),
              cost=cost)
```

---

### 📦 MODÜL 3: Frontend Dashboard Güncellemesi
| Alan | Detay |
|------|-------|
| **Ad** | React UI Extension |
| **Sorumlu Ajan** | Frontend Agent (Agent-2) |
| **Öncelik** | 🟡 YÜKSEK - Modül 2 ile paralel başlar |
| **Bağımlılık** | API kontratı netleşince başlar |

**Alt Görevler:**

#### 3A - services/api.js Güncelleme
```javascript
// services/api.js - Yeni metodlar
export const projectsAPI = {
  getAll: () => 
    api.get('/api/projects'),
  
  getById: (id) => 
    api.get(`/api/projects/${id}`),
  
  update: (id, data) => 
    api.patch(`/api/projects/${id}`, data),
  
  getAgentOutputs: (id) => 
    