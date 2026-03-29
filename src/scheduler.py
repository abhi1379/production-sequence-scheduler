"""Main scheduler interface"""

import csv
import json
from typing import Dict, List, Optional
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    pd = None

from src.models import (
    Product, ProductionLine, Material, Order, TimeWindow,
    ScheduleResult, ProductModel
)
from src.optimizer import ProductionOptimizer


class ProductionScheduler:
    """High-level scheduler API"""
    
    def __init__(self, time_horizon_hours: int = 24, time_step_minutes: int = 15):
        self.products: Dict[str, Product] = {}
        self.lines: Dict[str, ProductionLine] = {}
        self.materials: Dict[str, Material] = {}
        self.time_windows: List[TimeWindow] = []
        self.model_mix_targets: Dict[ProductModel, float] = {}
        self.optimizer = ProductionOptimizer(time_horizon_hours, time_step_minutes)
        self.latest_result: Optional[ScheduleResult] = None
    
    def add_product(self, product: Product):
        self.products[product.product_id] = product
    
    def add_line(self, line: ProductionLine):
        self.lines[line.line_id] = line
    
    def add_material(self, material: Material):
        self.materials[material.material_id] = material
    
    def add_time_window(self, window: TimeWindow):
        self.time_windows.append(window)
    
    def set_model_mix_target(self, targets: Dict[ProductModel, float]):
        self.model_mix_targets = targets
    
    def optimize(self, orders: List[Order], time_limit_seconds: int = 60) -> ScheduleResult:
        self.latest_result = self.optimizer.optimize(
            products=self.products, lines=self.lines, orders=orders,
            materials=self.materials, time_windows=self.time_windows,
            model_mix_targets=self.model_mix_targets if self.model_mix_targets else None,
            time_limit_seconds=time_limit_seconds
        )
        return self.latest_result
    
    def get_schedule_summary(self, result: Optional[ScheduleResult] = None) -> str:
        result = result or self.latest_result
        if not result:
            return "No schedule available"
        
        summary = []
        summary.append("=" * 70)
        summary.append("PRODUCTION SCHEDULE SUMMARY")
        summary.append("=" * 70)
        summary.append(f"\nStatus: {result.metrics.solver_status}")
        summary.append(f"Total Units Produced: {result.metrics.total_units_produced}")
        summary.append(f"Makespan: {result.metrics.makespan_hours:.1f} hours")
        summary.append(f"Avg Utilization: {result.metrics.avg_line_utilization:.1%}\n")
        
        summary.append(f"{'Seq':<4} {'Order':<10} {'Product':<10} {'Qty':<6} {'Line':<10}")
        summary.append("-" * 50)
        
        for item in sorted(result.schedule, key=lambda x: x.sequence_number):
            summary.append(
                f"{item.sequence_number:<4} {item.order_id:<10} {item.product_id:<10} "
                f"{item.quantity:<6} {item.line_id:<10}"
            )
        summary.append("=" * 70)
        return "\n".join(summary)
    
    def export_schedule_csv(self, result: Optional[ScheduleResult] = None, 
                           filename: str = "schedule.csv"):
        result = result or self.latest_result
        if not result:
            raise ValueError("No schedule to export")
        
        rows = []
        for item in result.schedule:
            rows.append({
                'Sequence': item.sequence_number,
                'Order ID': item.order_id,
                'Product ID': item.product_id,
                'Quantity': item.quantity,
            })
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"Schedule exported to {filename}")
    
    def export_schedule_json(self, result: Optional[ScheduleResult] = None,
                            filename: str = "schedule.json"):
        result = result or self.latest_result
        if not result:
            raise ValueError("No schedule to export")
        
        schedule_data = {
            'metrics': {
                'total_units_produced': result.metrics.total_units_produced,
                'makespan_hours': result.metrics.makespan_hours,
            },
            'schedule': [
                {
                    'sequence': item.sequence_number,
                    'order_id': item.order_id,
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                }
                for item in result.schedule
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(schedule_data, f, indent=2)
        print(f"Schedule exported to {filename}")
