import sqlite3
from pathlib import Path

def migrate_database():
    """Proje tablosuna yeni alanları ekle"""
    db_path = Path(__file__).parent / "projects.db"
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Mevcut sütunları kontrol et
        cursor.execute("PRAGMA table_info(projects)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        # Yeni sütunları ekle (eğer mevcut değilse)
        new_columns = [
            ("status", "TEXT DEFAULT 'active'"),
            ("phase", "TEXT DEFAULT 'planning'"),
            ("agent_outputs", "TEXT DEFAULT '{}'"),
            ("quality_score", "REAL DEFAULT 0.0"),
            ("cost", "REAL DEFAULT 0.0")
        ]
        
        for col_name, col_def in new_columns:
            if col_name not in existing_columns:
                cursor.execute(f"ALTER TABLE projects ADD COLUMN {col_name} {col_def}")
                print(f"Added column: {col_name}")
        
        conn.commit()
        print("Database migration completed successfully!")

if __name__ == "__main__":
    migrate_database()