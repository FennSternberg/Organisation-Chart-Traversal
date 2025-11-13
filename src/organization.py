from typing import Dict, List, Optional
from dataclasses import dataclass
import re
import warnings
def warning_format(message, category, filename, lineno, line=None):
    return f"Warning: {message}\n"

warnings.formatwarning = warning_format

def collapse_spaces(s: str) -> str:
    _SPACE_RE = re.compile(r"\s+")
    return _SPACE_RE.sub(" ", s.strip())

def normalize_name(name: str) -> str:
    """Normalize a name by removing extra spaces and converting to lowercase."""
    
    return collapse_spaces(name).lower()

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
        for e in employees.values():
            if e.manager_id is not None and e.manager_id in self.employees:
                self.children[e.manager_id].append(e.emp_id)
    
    @staticmethod
    def _process_file(path:str)->Dict[int, Employee]:
        """Process the input file and return a mapping of employee ID to Employee."""
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
                try:
                    emp_id = int(parts[1])
                except ValueError:
                    # Employee ID is missing
                    continue
                
                if emp_id in employees:
                    # Duplicate employee IDs are invalid
                    raise ValueError(f"Duplicate employee ID detected: {emp_id}")
                
                name = parts[2]
                manager_id = int(parts[3]) if parts[3] != "" else None

                name_normalized = normalize_name(name)

                employees[emp_id] = Employee(
                    emp_id=emp_id,
                    name_display=collapse_spaces(name),
                    name_normalized=name_normalized,
                    manager_id=manager_id,
                )
        return employees
    
    def roots(self) -> List[int]:
        """Return a list of root employee IDs (those without a manager)."""
        roots = []
        for eid, e in self.employees.items():
            if e.manager_id is None:
                roots.append(eid)
        return sorted(roots)
    
    def format_label(self, eid: int) -> str:
        e = self.employees[eid]
        return f"{e.name_display} ({e.emp_id})"
    
    def get_children(self, eid: int) -> List[int]:
        """Return a list of direct report employee IDs for the given employee ID."""
        return sorted(self.children.get(eid, []))
    
    def find_employee_ids_by_name(self, name) -> List[int]:
        """Find employee IDs matching the given name (case and space insensitive)."""
        ids = [e.emp_id for e in self.employees.values() if e.name_normalized == normalize_name(name)]
        return sorted(ids)
    
    def get_chain_to_root(self, eid: int, max_depth: int = 10000) -> List[int]:
        """Return the chain of employee IDs from the given employee to the root."""
        chain = []
        seen = set()
        current = eid
        depth = 0
        while current is not None:
            if current not in self.employees:
                raise ValueError(f"Employee ID {current} not found in organisation")
            
            if current in seen:
                raise ValueError("Cycle detected in management chain")
            seen.add(current)
            chain.append(current)
            current = self.employees[current].manager_id
            depth += 1
            if depth > max_depth:
                raise ValueError("Exceeded maximum chain depth")
        return chain
 
    @staticmethod
    def _lca_from_chains(chain_a: List[int], chain_b: List[int]) -> Optional[int]:
        """Return the lowest common ancestor from two chains to root."""
        set_b = set(chain_b)
        for eid in chain_a:
            if eid in set_b:
                return eid
        return None
        
    def format_path_between(self, a: int, b: int) -> str:
        """Format the communication path between two employee IDs."""
        if a == b:
            return self.format_label(a)
        chain_a = self.get_chain_to_root(a)
        chain_b = self.get_chain_to_root(b)
        lca = self._lca_from_chains(chain_a, chain_b)

        if not lca:
            raise ValueError("No communication path found between the two employees")
        
        # Upwards from a to LCA
        parts: List[str] = []
        for eid in chain_a:
            parts.append(self.format_label(eid))
            if eid == lca:
                break
            parts.append("->")
        
        # Downwards from LCA to b (excluding LCA)
        idx_lca_b = chain_b.index(lca)
        down = list(reversed(chain_b[:idx_lca_b]))
        for eid in down:
            parts.append("<-")
            parts.append(self.format_label(eid))
        return " ".join(parts)
            