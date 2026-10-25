from dataclasses import dataclass

@dataclass
class Budget:
    category: str
    monthly_limit: float