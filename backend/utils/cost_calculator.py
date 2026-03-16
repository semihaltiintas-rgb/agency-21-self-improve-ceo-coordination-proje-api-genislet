import json
from typing import Dict, Any

class CostCalculator:
    # Token maliyetleri (örnek fiyatlar)
    TOKEN_COSTS = {
        "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
        "gpt-3.5-turbo": {"input": 0.001 / 1000, "output": 0.002 / 1000},
        "claude": {"input": 0.008 / 1000, "output": 0.024 / 1000}
    }
    
    @staticmethod
    def calculate_project_cost(agent_outputs: Dict[str, Any]) -> float:
        """Proje maliyetini hesapla"""
        total_cost = 0.0
        
        for agent_name, output in agent_outputs.items():
            if isinstance(output, dict):
                token_usage = output.get("token_usage", {})
                model = output.get("model", "gpt-3.5-turbo")
                
                input_tokens = token_usage.get("input_tokens", 0)
                output_tokens = token_usage.get("output_tokens", 0)
                
                if model in CostCalculator.TOKEN_COSTS:
                    costs = CostCalculator.TOKEN_COSTS[model]
                    agent_cost = (
                        input_tokens * costs["input"] +
                        output_tokens * costs["output"]
                    )
                    total_cost += agent_cost
        
        return round(total_cost, 4)
    
    @staticmethod
    def estimate_cost(brief_length: int, complexity: str = "medium") -> float:
        """Proje maliyetini tahmin et"""
        complexity_multiplier = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.0
        }
        
        base_cost = brief_length * 0.0001  # Karakter başına base maliyet
        multiplier = complexity_multiplier.get(complexity, 1.0)
        
        return round(base_cost * multiplier, 4)