"""Example usage"""

from datetime import datetime, timedelta
from src.scheduler import ProductionScheduler
from src.models import (
    Product, ProductionLine, Material, Order,
    ProductModel, TimeWindow
)


def main():
    print("\n🏭 Production Sequence Scheduler - Demo\n")
    
    scheduler = ProductionScheduler(time_horizon_hours=24)
    
    prod_a = Product("PROD_A", ProductModel.MODEL_A,
                     bom={"STEEL": 10, "PLASTIC": 2},
                     processing_time=2.5, setup_time=30)
    scheduler.add_product(prod_a)
    
    prod_b = Product("PROD_B", ProductModel.MODEL_B,
                     bom={"STEEL": 15, "PLASTIC": 3},
                     processing_time=3.0, setup_time=25)
    scheduler.add_product(prod_b)
    
    line1 = ProductionLine("LINE_001", "Assembly Line 1",
                          capacity_units_per_hour=50, max_shift_hours=8.0,
                          models_supported=[ProductModel.MODEL_A, ProductModel.MODEL_B],
                          efficiency_factor=0.9)
    scheduler.add_line(line1)
    
    line2 = ProductionLine("LINE_002", "Assembly Line 2",
                          capacity_units_per_hour=45, max_shift_hours=8.0,
                          models_supported=[ProductModel.MODEL_A, ProductModel.MODEL_C],
                          efficiency_factor=0.85)
    scheduler.add_line(line2)
    
    steel = Material("STEEL", "Steel Stock", 5000.0, "kg")
    scheduler.add_material(steel)
    
    plastic = Material("PLASTIC", "Plastic Resin", 2000.0, "kg")
    scheduler.add_material(plastic)
    
    window = TimeWindow(datetime.now(), datetime.now() + timedelta(hours=8),
                       efficiency_factor=1.0)
    scheduler.add_time_window(window)
    
    scheduler.set_model_mix_target({
        ProductModel.MODEL_A: 0.5,
        ProductModel.MODEL_B: 0.3,
        ProductModel.MODEL_C: 0.2
    })
    
    orders = [
        Order("ORD001", prod_a, 500, datetime.now() + timedelta(days=1), priority=1),
        Order("ORD002", prod_b, 300, datetime.now() + timedelta(days=2), priority=2),
        Order("ORD003", prod_a, 400, datetime.now() + timedelta(days=3), priority=2),
    ]
    
    print("Running optimization...\n")
    result = scheduler.optimize(orders, time_limit_seconds=60)
    
    print(scheduler.get_schedule_summary(result))
    
    scheduler.export_schedule_csv(result, "schedule.csv")
    scheduler.export_schedule_json(result, "schedule.json")
    
    print("\n✅ Scheduling complete!")


if __name__ == "__main__":
    main()
