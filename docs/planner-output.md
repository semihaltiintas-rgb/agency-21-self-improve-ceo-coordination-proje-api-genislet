# PLANNER Çıktısı

# 📋 PROJE YÖNETİM PLANI: API Genişletme

## Proje Özeti & Kritik Yol Analizi

```
[MODÜL 1: DB Migration] → [MODÜL 2: Backend API] → [MODÜL 3B: UI Components]
         ↓                          ↓                         ↑
    (Bağımsız)            (M1 biter bitmez)          [MODÜL 3A: API Contract]
                                                       (M1 ile paralel)
```

**Toplam Tahmini Süre:** 6-8 saat (paralel çalışmayla)  
**Kritik Yol:** M1 → M2 → M3B (UI entegrasyon testi)

---

## 🔴 MODÜL 1: Database Migration
**Sorumlu:** DB Agent (Agent-3) | **Öncelik:** P0 - BLOCKER

---

### GÖREV 1.1 — Migration Script Yazımı
| Alan | Detay |
|------|-------|
| **Sorumlu** | DB Agent (Agent-3) |
| **Süre** | 30 dk |
| **Bağımlılık** | YOK — Başlangıç noktası |

**Kabul Kriterleri:**
- [ ] `migration_v2.py` dosyası oluşturuldu
- [ ] `BEGIN TRANSACTION / COMMIT` bloğu mevcut
- [ ] Tüm 5 ALTER TABLE komutu yazıldı
- [ ] `migration_history` tablosu CREATE IF NOT EXISTS ile oluşturuluyor
- [ ] Script idempotent (tekrar çalıştırılabilir, hata vermez)
- [ ] Rollback mekanizması mevcut

---

### GÖREV 1.2 — Migration Çalıştırma & Doğrulama
| Alan | Detay |
|------|-------|
| **Sorumlu** | DB Agent (Agent-3) |
| **Süre** | 20 dk |
| **Bağımlılık** | Görev 1.1 |

**Kabul Kriterleri:**
- [ ] `PRAGMA table_info(projects)` çıktısında 5 yeni sütun görünüyor
- [ ] Mevcut kayıtlar bozulmadı (NULL/DEFAULT değerler doğru)
- [ ] `migration_history` tablosunda `v2.0` kaydı var
- [ ] `projects.db` backup alındı (migration öncesi)
- [ ] Test: Yeni sütunlara INSERT/UPDATE başarılı

---

### GÖREV 1.3 — DB Katmanı (CRUD) Güncelleme
| Alan | Detay |
|------|-------|
| **Sorumlu** | DB Agent (Agent-3) |
| **Süre** | 40 dk |
| **Bağımlılık** | Görev 1.2 |

**Etkilenen Dosyalar:**
```
backend/
  ├── database.py          ← GÜNCELLE (yeni alanlar SELECT/INSERT'e ekle)
  ├── models.py            ← GÜNCELLE (ORM modeli genişlet)
  └── migration_v2.py      ← YENİ DOSYA
```

**Kabul Kriterleri:**
- [ ] `get_project()` fonksiyonu yeni alanları döndürüyor
- [ ] `update_project()` 5 yeni alan için UPDATE destekliyor
- [ ] `agent_outputs` JSON serialize/deserialize doğru çalışıyor
- [ ] `quality_score` 0.0-100.0 aralığı validasyonu var
- [ ] Tüm CRUD unit testleri geçiyor

---

## 🔴 MODÜL 2: Backend API Genişletme
**Sorumlu:** Backend Agent (Agent-1) | **Öncelik:** P0 - Modül 1 biter bitmez başlar

---

### GÖREV 2.1 — Pydantic Model Tanımları
| Alan | Detay |
|------|-------|
| **Sorumlu** | Backend Agent (Agent-1) |
| **Süre** | 30 dk |
| **Bağımlılık** | Görev 1.3 (DB modeli netleşmeli) |

**Etkilenen Dosyalar:**
```
backend/
  └── schemas.py           ← GÜNCELLE (veya YENİ DOSYA)
```

**Kabul Kriterleri:**
- [ ] `ProjectStatus` Enum tanımlı (5 değer)
- [ ] `ProjectPhase` Enum tanımlı (5 değer)
- [ ] `ProjectResponse` tüm alanları içeriyor
- [ ] `ProjectUpdateRequest` optional alanlarla tanımlı
- [ ] Pydantic validation testleri geçiyor
- [ ] `agent_outputs: Dict[str, Any]` JSON round-trip çalışıyor

---

### GÖREV 2.2 — Endpoint Güncelleme & Yeni Endpoint'ler
| Alan | Detay |
|------|-------|
| **Sorumlu** | Backend Agent (Agent-1) |
| **Süre** | 60 dk |
| **Bağımlılık** | Görev 2.1 |

**Etkilenen Dosyalar:**
```
backend/
  └── main.py              ← GÜNCELLE (endpoint'ler)
```

**Yeni/Değişen Endpoint Listesi:**
| Endpoint | Değişim |
|----------|---------|
| `GET /api/projects` | GÜNCELLE — yeni alanlar response'a eklenir |
| `GET /api/projects/{id}` | GÜNCELLE — detay + agent_outputs |
| `PATCH /api/projects/{id}` | YENİ — kısmi güncelleme |
| `GET /api/projects/{id}/agent-outputs` | YENİ |
| `POST /api/run` | GÜNCELLE — status/phase lifecycle |
| `GET /api/projects/stats/summary` | YENİ — dashboard aggregate |

**Kabul Kriterleri:**
- [ ] Tüm endpoint'ler Swagger UI'da görünüyor
- [ ] `PATCH` sadece gönderilen alanları güncelliyor
- [ ] `POST /api/run` status: `pending→running`, phase: `init→execution` geçişi yapıyor
- [ ] `GET /stats/summary` aggregate hesaplamalar doğru
- [ ] 404 ve hata response'ları standart formatta
- [ ] Response time < 200ms (DB query optimizasyonu)

---

### GÖREV 2.3 — Ajan Output Mekanizması
| Alan | Detay |
|------|-------|
| **Sorumlu** | Backend Agent (Agent-1) |
| **Süre** | 45 dk |
| **Bağımlılık** | Görev 2.2 |

**Etkilenen Dosyalar:**
```
backend/
  ├── main.py              ← GÜNCELLE
  └── utils/
      ├── cost_calculator.py   ← YENİ DOSYA
      └── quality_scorer.py    ← YENİ DOSYA
```

**Kabul Kriterleri:**
- [ ] `update_agent_output()` her ajan tamamlandığında çağrılıyor
- [ ] `agent_outputs` JSON yapısı: `{agent_id: {output, completed_at, tokens_used