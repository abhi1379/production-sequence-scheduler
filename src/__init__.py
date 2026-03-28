# Core Data Models

# This file includes classes and functions for core data models used in the production sequence scheduler.

class CoreDataModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Product(CoreDataModel):
    def __init__(self, id, name, quantity):
        super().__init__(id, name)
        self.quantity = quantity

# Additional models can be added here.