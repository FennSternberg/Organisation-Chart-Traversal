from typing import Dict, List, Optional
from dataclasses import dataclass
import re

@dataclass
class Employee:
    """Class representing an employee in the organisation."""
    emp_id: int
    name_display: str
    name_normalized: str
    manager_id: Optional[int]


class Organization:
    """Class representing the organisation structure."""
    def __init__(self, path: str):
        employees = self._process_file(path)
        self.employees: Dict[int, Employee] = employees
        self.children: Dict[int, List[int]] = {eid: [] for eid in employees}
    
    def _process_file(self, path:str)->Dict[int, Employee]:
        # Implementation to read file and create employees dictionary
        employees: Dict[int, Employee] = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    # Skip empty lines
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) < 4:
                    continue
                if parts[1].lower() == "employee id":
                    # header row
                    continue

                emp_id = int(parts[1])
                name = parts[2]
                manager_id = int(parts[3]) if parts[3] != "" else None

                _SPACE_RE = re.compile(r"\s+")
                name_normalized = _SPACE_RE.sub(" ", name).strip().lower()

                employees[emp_id] = Employee(
                    emp_id=emp_id,
                    name_display=name,
                    name_normalized=name_normalized,
                    manager_id=manager_id,
                )
        return employees



    