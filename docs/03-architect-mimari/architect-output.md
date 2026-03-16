# ARCHITECT Çıktısı



# 🏗️ Teknik Mimari: Proje API Genişletme

## 1. Proje Klasör Yapısı

```
project-manager/
├── backend/
│   ├── __init__.py
│   ├── main.py                          # FastAPI ana uygulama (GÜNCELLE)
│   ├── database.py                      # DB bağlantı + CRUD (GÜNCELLE)
│   ├── models.py                        # SQLAlchemy ORM modelleri (GÜNCELLE)
│   ├── schemas.py                       # Pydantic şemaları (YENİ)
│   ├── config.py                        # Uygulama konfigürasyonu (YENİ)
│   ├── migration_v2.py                  # Migration script (YENİ)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cost_calculator.py           # Maliyet hesaplama (YENİ)
│   │   └── quality_scorer.py            # Kalite skorlama (YENİ)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── projects.py                  # Proje endpoint'leri (YENİ - refactor)
│   │   ├── agents.py                    # Agent output endpoint'leri (YENİ)
│   │   └── stats.py                     # İstatistik endpoint'leri (YENİ)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_migration.py            # Migration testleri
│   │   ├── test_crud.py                 # CRUD testleri
│   │   ├── test_projects_api.py         # API endpoint testleri
│   │   ├── test_schemas.py              # Pydantic validation testleri
│   │   └── conftest.py                  # Test fixtures
│   ├── projects.db                      # SQLite veritabanı
│   ├── projects_backup_v1.db            # Migration öncesi backup
│   └── requirements.txt                 # Python bağımlılıkları
├── frontend/
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── main.jsx                     # React entry point
│   │   ├── App.jsx                      # Router tanımları (GÜNCELLE)
│   │   ├── api/
│   │   │   ├── client.js                # Axios instance (GÜNCELLE)
│   │   │   ├── projects.js              # Proje API fonksiyonları (GÜNCELLE)
│   │   │   └── stats.js                 # İstatistik API fonksiyonları (YENİ)
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Header.jsx
│   │   │   ├── projects/
│   │   │   │   ├── ProjectCard.jsx      # GÜNCELLE (status badge, quality)
│   │   │   │   ├── ProjectStatusBadge.jsx  # YENİ
│   │   │   │   ├── ProjectPhaseBadge.jsx   # YENİ
│   │   │   │   ├── QualityScoreRing.jsx    # YENİ
│   │   │   │   ├── CostDisplay.jsx         # YENİ
│   │   │   │   └── AgentOutputPanel.jsx    # YENİ
│   │   │   ├── dashboard/
│   │   │   │   ├── StatsSummaryCards.jsx   # YENİ
│   │   │   │   ├── ProjectsOverviewChart.jsx # YENİ
│   │   │   │   └── RecentActivity.jsx      # YENİ
│   │   │   └── common/
│   │   │       ├── LoadingSpinner.jsx
│   │   │       ├── ErrorBoundary.jsx
│   │   │       └── ProgressBar.jsx         # YENİ
│   │   ├── hooks/
│   │   │   ├── useProjects.js           # GÜNCELLE
│   │   │   ├── useProjectDetail.js      # YENİ
│   │   │   └── useDashboardStats.js     # YENİ
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx            # GÜNCELLE (stats entegrasyonu)
│   │   │   ├── ChatPage.jsx
│   │   │   ├── ProjectsPage.jsx         # GÜNCELLE (filtreleme + yeni alanlar)
│   │   │   ├── ProjectDetail.jsx        # GÜNCELLE (agent outputs, quality, cost)
│   │   │   ├── NewProject.jsx
│   │   │   └── AgentPanel.jsx           # GÜNCELLE (output gösterimi)
│   │   ├── constants/
│   │   │   └── projectEnums.js          # YENİ (status, phase sabitleri)
│   │   └── styles/
│   │       └── globals.css
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── docker-compose.yml                   # Opsiyonel
├── Makefile                             # Build/migration komutları
└── README.md
```

---

## 2. Bağımlılık Dosyaları

### `backend/requirements.txt`

```txt
# === Core Framework ===
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
pydantic-settings==2.1.0

# === Database ===
sqlalchemy==2.0.23
aiosqlite==0.19.0
alembic==1.13.0

# === Serialization & Validation ===
python-dateutil==2.8.2
orjson==3.9.10

# === CORS & Middleware ===
python-multipart==0.0.6

# === Testing ===
pytest==7.4.3
pytest-asyncio==0.23.2
httpx==0.25.2

# === Utilities ===
loguru==0.7.2
```

### `frontend/package.json`

```json
{
  "name": "project-manager-frontend",
  "private": true,
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.1",
    "axios": "^1.6.2",
    "lucide-react": "^0.303.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.2.0",
    "date-fns": "^3.0.6",
    "recharts": "^2.10.3",
    "react-hot-toast": "^2.4.1",
    "swr": "^2.2.4",
    "@tanstack/react-query": "^5.17.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.8"
  }
}
```

---

## 3. Temel Konfigürasyon Dosyaları

### `backend/config.py`

```python
"""
Uygulama konfigürasyonu.
Çevre değişkenleri veya .env dosyasından okunur.
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    # === Uygulama ===
    APP_NAME: str = "Project Manager API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # === Veritabanı ===
    DATABASE_URL: str = "sqlite+aiosqlite:///./projects.db"
    DATABASE_SYNC_URL: str = "sqlite:///./projects.db"
    DB_BACKUP_DIR: str = "./backups"

    # === API ===
    API_PREFIX: str = "/api"
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    # === Maliyet Hesaplama ===
    COST_PER_INPUT_TOKEN: float = 0.00001    # $0.01/1K token
    COST_PER_OUTPUT_TOKEN: float = 0.00003   # $0.03/1K token
    DEFAULT_CURRENCY: str = "USD"

    # === Kalite Skoru ===
    QUALITY_SCORE_MIN: float = 0.0
    QUALITY_SCORE_MAX: float = 100.0

    # === Migration ===
    CURRENT_DB_VERSION: str = "2.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

### `backend/models.py`

```python
"""
SQLAlchemy ORM modelleri.
V2: status, phase, agent_outputs, quality_score, cost alanları eklendi.
"""
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime,
    Enum as SAEnum, JSON, Boolean, Index, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


# ============================================================
# ENUM TANIMLARI
# ============================================================

class ProjectStatus(str, enum.Enum):
    """Proje durum makinesi."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProjectPhase(str, enum.Enum):
    """Proje aşama makinesi."""
    INIT = "init"
    PLANNING = "planning"
    EXECUTION = "execution"
    REVIEW = "review"
    DONE = "done"


# ============================================================
# PROJE MODELİ
# ============================================================

class Project(Base):
    __tablename__ = "projects"

    # --- Mevcut alanlar (V1) ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # --- Yeni alanlar (V2) ---
    status: Mapped[str] = mapped_column(
        String(20),
        default=ProjectStatus.PENDING.value,
        nullable=False,
        index=True
    )
    phase: Mapped[str] = mapped_column(
        String(20),
        default=ProjectPhase.INIT.value,
        nullable=False,
        index=True
    )
    agent_outputs: Mapped[Optional[dict]] = mapped_column(
        JSON,
        default=dict,
        nullable=True
    )
    quality_score: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        nullable=True
    )
    cost: Mapped[Optional[float]] = mapped_column(
        Float,
        default=0.0,
        nullable=True
    )

    # --- Tablo kısıtları ---
    __table_args__ = (
        CheckConstraint(
            "quality_score IS NULL OR (quality_score >= 0.0 AND quality_score <= 100.0)",
            name="check_quality_score_range"
        ),
        CheckConstraint(
            "cost IS NULL OR cost >= 0.0",
            name="check_cost_non_negative"
        ),
        CheckConstraint(
            f"status IN ('{ProjectStatus.PENDING.value}', '{ProjectStatus.RUNNING.value}', "
            f"'{ProjectStatus.COMPLETED.value}', '{ProjectStatus.FAILED.value}', "
            f"'{ProjectStatus.CANCELLED.value}')",
            name="check_valid_status"
        ),
        CheckConstraint(
            f"phase IN ('{ProjectPhase.INIT.value}', '{ProjectPhase.PLANNING.value}', "
            f"'{ProjectPhase.EXECUTION.value}', '{ProjectPhase.REVIEW.value}', "
            f"'{ProjectPhase.DONE.value}')",
            name="check_valid_phase"
        ),
        Index("idx_status_phase", "status", "phase"),
    )

    def __repr__(self) -> str:
        return (
            f"<Project(id={self.id}, name='{self.name}', "
            f"status='{self.status}', phase='{self.phase}')>"
        )


# ============================================================
# MİGRATİON GEÇMİŞİ
# ============================================================

class MigrationHistory(Base):
    __tablename__ = "migration_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    success: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

### `backend/schemas.py`

```python
"""
Pydantic V2 şemaları.
Request/Response model tanımları, validasyon kuralları.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_