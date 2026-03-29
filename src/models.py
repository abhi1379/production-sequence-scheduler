"""
Data models for production sequence scheduling
"""

from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field


class ProductModel(str, Enum):
    """Product models/variants"""
    MODEL_A = "MODEL_A"
    MODEL_B = "MODEL_B"
    MODEL_C = "MODEL_C"
    MODEL_D = "MODEL_D"


@dataclass
class Material:
    """Material tracking and availability"""
    material_id: str
    name: str
    available_quantity: float
    unit: str = "kg"
    reorder_level: float = 0.0
    
    def is_available(self, quantity: float) -> bool:
        return self.available_quantity >= quantity
    
    def consume(self, quantity: float) -> bool:
        if self.is_available(quantity):
            self.available_quantity -= quantity
            return True
        return False
    
    def restock(self, quantity: float):
        self.available_quantity += quantity


@dataclass
class Product:
    """Product definition with BOM"""
    product_id: str
    model: ProductModel
    bom: Dict[str, float]
    processing_time: float
    setup_time: float = 30.0
    quality_check_time: float = 2.0
    
    def get_materials_required(self, quantity: int) -> Dict[str, float]:
        return {mat_id: qty * quantity for mat_id, qty in self.bom.items()}


@dataclass
class ProductionLine:
    """Production line definition"""
    line_id: str
    name: str
    capacity_units_per_hour: float
    max_shift_hours: float = 8.0
    models_supported: List[ProductModel] = field(default_factory=list)
    efficiency_factor: float = 1.0
    
    @property
    def effective_capacity(self) -> float:
        return self.capacity_units_per_hour * self.efficiency_factor
    
    @property
    def max_daily_capacity(self) -> float:
        return self.effective_capacity * self.max_shift_hours
    
    def can_produce(self, model: ProductModel) -> bool:
        if not self.models_supported:
            return True
        return model in self.models_supported


@dataclass
class Order:
    """Production order"""
    order_id: str
    product: Product
    quantity: int
    due_date: datetime
    priority: int = 1


@dataclass
class TimeWindow:
    """Production time window"""
    start_time: datetime
    end_time: datetime
    efficiency_factor: float = 1.0


@dataclass
class ScheduleItem:
    """Scheduled task"""
    sequence_number: int
    order_id: str
    product_id: str
    model: ProductModel
    line_id: str
    start_time: datetime
    end_time: datetime
    quantity: int
    setup_time_minutes: float = 0.0
    processing_time_minutes: float = 0.0
    materials_used: Dict[str, float] = field(default_factory=dict)


@dataclass
class OptimizationMetrics:
    """Metrics from optimization"""
    total_orders_completed: int
    total_units_produced: int
    makespan_hours: float
    line_utilization: Dict[str, float]
    avg_line_utilization: float
    schedule_feasibility: bool
    objective_value: float
    solver_status: str = "OPTIMAL"


@dataclass
class ScheduleResult:
    """Optimization result"""
    schedule: List[ScheduleItem]
    metrics: OptimizationMetrics
    feasible: bool
    objective_value: float
