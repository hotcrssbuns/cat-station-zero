from enum import Enum
from typing import Dict, List


class Priority(Enum):
    CRITICAL = "CRITICAL"
    URGENT = "URGENT"
    ROUTINE = "ROUTINE"


class Task:
    def __init__(
        self,
        name,
        description,
        priority,
        required_resources,
        turns_to_complete,
        success_effects,
        failure_effects,
    ):
        self.name = name
        self.description = description
        self.priority = priority
        self.required_resources = required_resources
        self.turns_to_complete = turns_to_complete
        self.success_effects = success_effects
        self.failure_effects = failure_effects
        self.turns_remaining = turns_to_complete

    def __str__(self):
        return f"{self.priority.value}: {self.name} ({self.turns_remaining} turns left)"


class TaskManager:
    def __init__(self):
        self.active_tasks: List[Task] = []
        self.task_templates = {
            "repair_oxygen": {
                "name": "Repair Oxygen Recycler",
                "description": "The oxygen recycling system is malfunctioning and needs repairs.",
                "priority": Priority.CRITICAL,
                "required_resources": {"spare_parts": 2},
                "turns_to_complete": 3,
                "success_effects": {"oxygen": 15},
                "failure_effects": {"oxygen": -10},
            },
            "boost_power": {
                "name": "Emergency Power Boost",
                "description": "Station power levels are dropping. Install backup power cells.",
                "priority": Priority.URGENT,
                "required_resources": {"power_cells": 1},
                "turns_to_complete": 2,
                "success_effects": {"power": 20},
                "failure_effects": {"power": -5},
            },
        }
