import json
import re
from typing import Dict, Any

class QualityScorer:
    @staticmethod
    def calculate_quality_score(code: str, agent_outputs: Dict[str, Any]) -> float:
        """Kod kalitesi skorunu hesapla (0-100 arası)"""
        if not code:
            return 0.0
            
        score = 0.0
        
        # Kod yapısı kontrolü (40 puan)
        score += QualityScorer._check_code_structure(code)
        
        # Agent başarı oranı (30 puan)
        score += QualityScorer._check_agent_success(agent_outputs)
        
        # Kod kompleksitesi (20 puan)
        score += QualityScorer._check_complexity(code)
        
        # Best practices (10 puan)
        score += QualityScorer._check_best_practices(code)
        
        return min(100.0, max(0.0, score))
    
    @staticmethod
    def _check_code_structure(code: str) -> float:
        """Kod yapısını kontrol et"""
        score = 0.0
        
        # Bileşen tanımları var mı?
        if re.search(r'function\s+\w+|const\s+\w+\s*=', code):
            score += 15
        
        # Import/export yapısı
        if 'import' in code and 'export' in code:
            score += 10
        
        # JSX kullanımı
        if '<' in code and '/>' in code:
            score += 10
        
        # Error handling
        if 'try' in code or 'catch' in code:
            score += 5
        
        return score
    
    @staticmethod
    def _check_agent_success(agent_outputs: Dict[str, Any]) -> float:
        """Agent başarı oranını kontrol et"""
        if not agent_outputs:
            return 15.0  # Varsayılan orta değer
            
        success_count = 0
        total_agents = len(agent_outputs)
        
        for output in agent_outputs.values():
            if isinstance(output, dict):
                if output.get("status") == "success":
                    success_count += 1
        
        if total_agents == 0:
            return 15.0
            
        success_rate = success_count / total_agents
        return success_rate * 30
    
    @staticmethod
    def _check_complexity(code: str) -> float:
        """Kod kompleksitesini değerlendir"""
        lines = len(code.split('\n'))
        functions = len(re.findall(r'function\s+\w+|const\s+\w+\s*=.*=>', code))
        
        if lines > 200 and functions > 5:
            return 20  # Yüksek kompleksite
        elif lines > 100 and functions > 3:
            return 15  # Orta kompleksite
        elif lines > 50:
            return 10  # Düşük kompleksite
        else:
            return 5   # Çok basit
    
    @staticmethod
    def _check_best_practices(code: str) -> float:
        """Best practices kontrolü"""
        score = 0.0
        
        # Const/let kullanımı (var yerine)
        if 'const ' in code or 'let ' in code:
            score += 3
        
        # Arrow functions
        if '=>' in code:
            score += 2
        
        # Destructuring
        if '...' in code or re.search(r'\{[^}]+\}\s*=', code):
            score += 3
        
        # Comments
        if '//' in code or '/*' in code:
            score += 2
        
        return score