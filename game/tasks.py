from enum import Enum
from typing import Dict, List
import random


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
        self.resources_assigned = False

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
            "fix_cat_flap": {
                "name": "Fix Emergency Cat Flap",
                "description": "The emergency escape flap is jammed. Critical for cat safety!",
                "priority": Priority.CRITICAL,
                "required_resources": {"spare_parts": 1, "crew_members": 2},
                "turns_to_complete": 2,
                "success_effects": {"hull_integrity": 10, "crew_morale": 5},
                "failure_effects": {"hull_integrity": -15},
            },
            "heal_injured_cat": {
                "name": "Treat Injured Crew Member",
                "description": "A cat crew member was injured during the last maintenance round.",
                "priority": Priority.URGENT,
                "required_resources": {"medical_supplies": 1, "crew_members": 1},
                "turns_to_complete": 2,
                "success_effects": {"crew_morale": 15},
                "failure_effects": {"crew_morale": -10},
            },
            "repair_hull_breach": {
                "name": "Seal Hull Breach",
                "description": "Critical hull breach detected in sector 7!",
                "priority": Priority.CRITICAL,
                "required_resources": {"spare_parts": 3, "crew_members": 2},
                "turns_to_complete": 3,
                "success_effects": {"hull_integrity": 25},
                "failure_effects": {"hull_integrity": -20, "oxygen": -10},
            },
            "recalibrate_sensors": {
                "name": "Recalibrate Mouse Detection Grid",
                "description": "The station's rodent detection sensors need adjustment.",
                "priority": Priority.ROUTINE,
                "required_resources": {"spare_parts": 1, "crew_members": 1},
                "turns_to_complete": 2,
                "success_effects": {"hull_integrity": 5, "crew_morale": 5},
                "failure_effects": {"crew_morale": -5},
            },
            "emergency_power_reroute": {
                "name": "Reroute Emergency Power",
                "description": "Power systems failing in critical areas!",
                "priority": Priority.CRITICAL,
                "required_resources": {"power_cells": 2, "crew_members": 2},
                "turns_to_complete": 2,
                "success_effects": {"power": 25},
                "failure_effects": {"power": -15},
            },
            "clean_filters": {
                "name": "Clean Air Filters",
                "description": "Air filters clogged with cat hair.",
                "priority": Priority.ROUTINE,
                "required_resources": {"crew_members": 1},
                "turns_to_complete": 1,
                "success_effects": {"oxygen": 10},
                "failure_effects": {"oxygen": -5},
            },
            "repair_food_replicator": {
                "name": "Fix Kibble Replicator",
                "description": "The food replication system is producing bland kibble.",
                "priority": Priority.URGENT,
                "required_resources": {"spare_parts": 1, "power_cells": 1},
                "turns_to_complete": 2,
                "success_effects": {"crew_morale": 15},
                "failure_effects": {"crew_morale": -10},
            },
            "stabilize_life_support": {
                "name": "Stabilize Life Support",
                "description": "Life support systems showing dangerous fluctuations!",
                "priority": Priority.CRITICAL,
                "required_resources": {"power_cells": 2, "spare_parts": 2},
                "turns_to_complete": 3,
                "success_effects": {"oxygen": 20, "power": 10},
                "failure_effects": {"oxygen": -15, "power": -10},
            },
            "treat_space_sickness": {
                "name": "Treat Space Motion Sickness",
                "description": "Several crew members have developed space sickness.",
                "priority": Priority.URGENT,
                "required_resources": {"medical_supplies": 2},
                "turns_to_complete": 2,
                "success_effects": {"crew_morale": 15},
                "failure_effects": {"crew_morale": -10},
            },
            "upgrade_scratching_post": {
                "name": "Reinforce Anti-Grav Scratching Posts",
                "description": "Zero-G scratching posts showing wear and tear.",
                "priority": Priority.ROUTINE,
                "required_resources": {"spare_parts": 1},
                "turns_to_complete": 1,
                "success_effects": {"crew_morale": 10},
                "failure_effects": {"crew_morale": -5},
            },
            "repair_heating": {
                "name": "Fix Climate Control",
                "description": "Station getting too cold for comfortable cat naps.",
                "priority": Priority.URGENT,
                "required_resources": {"power_cells": 1, "spare_parts": 1},
                "turns_to_complete": 2,
                "success_effects": {"crew_morale": 10, "power": 5},
                "failure_effects": {"crew_morale": -10, "power": -5},
            },
            "maintenance_check": {
                "name": "Routine Maintenance Check",
                "description": "Perform standard system diagnostics.",
                "priority": Priority.ROUTINE,
                "required_resources": {"crew_members": 1},
                "turns_to_complete": 1,
                "success_effects": {"hull_integrity": 5, "power": 5},
                "failure_effects": {"power": -5},
            },
            "emergency_surgery": {
                "name": "Perform Emergency Surgery",
                "description": "Crew member requires immediate medical attention!",
                "priority": Priority.CRITICAL,
                "required_resources": {"medical_supplies": 3, "crew_members": 2},
                "turns_to_complete": 3,
                "success_effects": {"crew_morale": 20},
                "failure_effects": {"crew_morale": -25},
            },
            "calibrate_gravity": {
                "name": "Calibrate Anti-Grav Systems",
                "description": "Gravity fluctuations causing chaos with the cat toys!",
                "priority": Priority.URGENT,
                "required_resources": {"power_cells": 1, "crew_members": 1},
                "turns_to_complete": 2,
                "success_effects": {"hull_integrity": 10, "crew_morale": 5},
                "failure_effects": {"hull_integrity": -5, "crew_morale": -10},
            },
            "repair_comms": {
                "name": "Repair Communication Array",
                "description": "Long-range communication system failure.",
                "priority": Priority.URGENT,
                "required_resources": {"spare_parts": 2, "power_cells": 1},
                "turns_to_complete": 3,
                "success_effects": {"power": 10, "crew_morale": 5},
                "failure_effects": {"power": -10, "crew_morale": -5},
            },
            "organize_supplies": {
                "name": "Organize Supply Storage",
                "description": "Crew members knocked supplies off shelves again.",
                "priority": Priority.ROUTINE,
                "required_resources": {"crew_members": 1},
                "turns_to_complete": 1,
                "success_effects": {"crew_morale": 5},
                "failure_effects": {"crew_morale": -5},
            },
            "radiation_shields": {
                "name": "Strengthen Radiation Shields",
                "description": "Dangerous radiation levels detected!",
                "priority": Priority.CRITICAL,
                "required_resources": {"spare_parts": 2, "power_cells": 2},
                "turns_to_complete": 3,
                "success_effects": {"hull_integrity": 20, "power": 10},
                "failure_effects": {"hull_integrity": -15, "power": -10},
            },
            "upgrade_beds": {
                "name": "Upgrade Crew Quarters",
                "description": "Sleeping pods need more comfortable cushions.",
                "priority": Priority.ROUTINE,
                "required_resources": {"spare_parts": 1},
                "turns_to_complete": 2,
                "success_effects": {"crew_morale": 15},
                "failure_effects": {"crew_morale": -5},
            },
        }

    def create_task(self) -> Task:
        available_tasks = list(self.task_templates.keys())
        task_id = random.choice(available_tasks)
        template = self.task_templates[task_id]
        new_task = Task(**template)
        self.active_tasks.append(new_task)
        return new_task

    def get_active_tasks(self) -> List[Task]:
        return self.active_tasks

    def remove_task(self, task: Task):
        if task in self.active_tasks:
            self.active_tasks.remove(task)
