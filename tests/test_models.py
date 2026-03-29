"""Unit tests for models"""

import pytest
from datetime import datetime, timedelta
from src.models import (
    Material, Product, ProductionLine, Order,
    ProductModel, TimeWindow
)


class TestMaterial:
    def test_material_creation(self):
        mat = Material("MAT001", "Steel", 1000.0, "kg")
        assert mat.material_id == "MAT001"
        assert mat.available_quantity == 1000.0
    
    def test_material_availability(self):
        mat = Material("MAT001", "Steel", 1000.0)
        assert mat.is_available(500.0) is True
        assert mat.is_available(1500.0) is False
    
    def test_material_consume(self):
        mat = Material("MAT001", "Steel", 1000.0)
        result = mat.consume(300.0)
        assert result is True
        assert mat.available_quantity == 700.0


class TestProduct:
    def test_product_creation(self):
        bom = {"MAT001": 10.0, "MAT002": 5.0}
        product = Product("PROD001", ProductModel.MODEL_A, bom, 2.5)
        assert product.product_id == "PROD001"
        assert product.model == ProductModel.MODEL_A


class TestProductionLine:
    def test_line_creation(self):
        line = ProductionLine("LINE001", "Line 1", 50.0, 8.0)
        assert line.line_id == "LINE001"
        assert line.max_daily_capacity == 400.0
