from typing import Dict, List, Optional
class Employee:
    """Class representing an employee in the organisation."""
    emp_id: int
    name_display: str
    name_normalized: str
    manager_id: Optional[int]


class Organisation:
    """Class representing the organisation structure."""
    def __init__(self, path: str):
        employees = self._process_file(path)
        self.employees: Dict[int, Employee] = employees
        self.children: Dict[int, List[int]] = {eid: [] for eid in employees}
    
    def _process_file(path:str)->Dict[int, Employee]:
        # Implementation to read file and create employees dictionary
        pass

    