import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

class Database:
    def __init__(self, db_name="projects.db"):
        self.db_path = Path(__file__).parent / db_name
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brief TEXT NOT NULL,
                    code TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    phase TEXT DEFAULT 'planning',
                    agent_outputs TEXT DEFAULT '{}',
                    quality_score REAL DEFAULT 0.0,
                    cost REAL DEFAULT 0.0
                )
            """)
            conn.commit()
    
    def create_project(self, brief: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (brief) 
                VALUES (?)
            """, (brief,))
            project_id = cursor.lastrowid
            conn.commit()
            
        return self.get_project(project_id)
    
    def get_projects(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, brief, code, created_at, updated_at, status, phase, 
                       agent_outputs, quality_score, cost
                FROM projects 
                ORDER BY updated_at DESC
            """)
            
            projects = []
            for row in cursor.fetchall():
                try:
                    agent_outputs = json.loads(row[7]) if row[7] else {}
                except:
                    agent_outputs = {}
                    
                projects.append({
                    'id': row[0],
                    'brief': row[1],
                    'code': row[2],
                    'created_at': row[3],
                    'updated_at': row[4],
                    'status': row[5],
                    'phase': row[6],
                    'agent_outputs': agent_outputs,
                    'quality_score': row[8],
                    'cost': row[9]
                })
            
            return projects
    
    def get_project(self, project_id: int) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, brief, code, created_at, updated_at, status, phase,
                       agent_outputs, quality_score, cost
                FROM projects 
                WHERE id = ?
            """, (project_id,))
            
            row = cursor.fetchone()
            if row:
                try:
                    agent_outputs = json.loads(row[7]) if row[7] else {}
                except:
                    agent_outputs = {}
                    
                return {
                    'id': row[0],
                    'brief': row[1],
                    'code': row[2],
                    'created_at': row[3],
                    'updated_at': row[4],
                    'status': row[5],
                    'phase': row[6],
                    'agent_outputs': agent_outputs,
                    'quality_score': row[8],
                    'cost': row[9]
                }
        return None
    
    def update_project(self, project_id: int, updates: Dict[str, Any]) -> Optional[dict]:
        if not updates:
            return self.get_project(project_id)
            
        # Agent outputs'u JSON string'e çevir
        if 'agent_outputs' in updates:
            updates['agent_outputs'] = json.dumps(updates['agent_outputs'])
        
        # Updated_at'ı güncelle
        updates['updated_at'] = datetime.now().isoformat()
        
        # Update sorgusu oluştur
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [project_id]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE projects 
                SET {set_clause}
                WHERE id = ?
            """, values)
            conn.commit()
            
        return self.get_project(project_id)
    
    def get_project_stats(self) -> Dict[str, Any]:
        """Proje istatistiklerini getir"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Toplam proje sayısı
            cursor.execute("SELECT COUNT(*) FROM projects")
            total_projects = cursor.fetchone()[0]
            
            # Status'a göre dağılım
            cursor.execute("""
                SELECT status, COUNT(*) 
                FROM projects 
                GROUP BY status
            """)
            status_distribution = dict(cursor.fetchall())
            
            # Phase'e göre dağılım
            cursor.execute("""
                SELECT phase, COUNT(*) 
                FROM projects 
                GROUP BY phase
            """)
            phase_distribution = dict(cursor.fetchall())
            
            # Ortalama kalite skoru
            cursor.execute("SELECT AVG(quality_score) FROM projects WHERE quality_score > 0")
            avg_quality = cursor.fetchone()[0] or 0.0
            
            # Toplam maliyet
            cursor.execute("SELECT SUM(cost) FROM projects")
            total_cost = cursor.fetchone()[0] or 0.0
            
            return {
                'total_projects': total_projects,
                'status_distribution': status_distribution,
                'phase_distribution': phase_distribution,
                'avg_quality_score': round(avg_quality, 2),
                'total_cost': round(total_cost, 4)
            }