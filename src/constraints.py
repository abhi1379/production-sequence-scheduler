"""Constraint engine"""

from typing import Dict, List
from dataclasses import dataclass
from src.models import Product, ProductionLine, Material, TimeWindow, ScheduleItem, ProductModel


@dataclass
class ConstraintViolation:
    constraint_type: str
    severity: str
    description: str
    entity_id: str
    penalty: float = 0.0


class ConstraintEngine:
    """Manages scheduling constraints"""
    
    def __init__(self):
        self.violations: List[ConstraintViolation] = []
        self.material_inventory: Dict[str, float] = {}
        self.line_capacity_used: Dict[str, float] = {}
        self.time_windows: List[TimeWindow] = []
        self.model_mix_targets: Dict[ProductModel, float] = {}
    
    def add_material_constraint(self, materials: Dict[str, Material]):
        self.material_inventory = {
            mat_id: mat.available_quantity for mat_id, mat in materials.items()
        }
    
    def add_line_capacity_constraint(self, lines: List[ProductionLine]):
        self.line_capacity_used = {line.line_id: 0.0 for line in lines}
    
    def add_time_window_constraint(self, windows: List[TimeWindow]):
        self.time_windows = windows
    
    def add_model_mix_constraint(self, targets: Dict[ProductModel, float]):
        self.model_mix_targets = targets
    
    def validate_material_availability(self, product: Product, quantity: int, 
                                      available_materials: Dict[str, Material]) -> bool:
        materials_needed = product.get_materials_required(quantity)
        for material_id, needed_qty in materials_needed.items():
            if material_id not in available_materials:
                return False
            material = available_materials[material_id]
            if not material.is_available(needed_qty):
                return False
        return True
    
    def clear_violations(self):
        self.violations.clear()
