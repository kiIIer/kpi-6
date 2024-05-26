import geopandas as gpd
import matplotlib.pyplot as plt
from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
import copy

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        pass


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        self.iterations = 0
        self.failures = 0
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP", variable, self.variables)
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def order_domain_values(self, variable: V, assignment: Dict[V, D]) -> List[D]:
        if variable in assignment:
            return []

        def count_conflicts(value: D) -> int:
            local_assignment = assignment.copy()
            local_assignment[variable] = value
            conflicts = 0
            for v in self.variables:
                if v != variable and v not in assignment and not self.consistent(v, local_assignment):
                    conflicts += 1
            return conflicts

        return sorted(self.domains[variable], key=count_conflicts)

    def select_unassigned_variable(self, assignment: Dict[V, D]) -> V:
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def forward_checking(self, variable: V, value: D, assignment: Dict[V, D], domains: Dict[V, List[D]]) -> bool:
        local_assignment = assignment.copy()
        local_assignment[variable] = value
        for neighbor in self.variables:
            if neighbor != variable and neighbor not in local_assignment:
                for neighbor_value in domains[neighbor][:]:
                    local_assignment[neighbor] = neighbor_value
                    if not self.consistent(neighbor, local_assignment):
                        domains[neighbor].remove(neighbor_value)
                    local_assignment.pop(neighbor)
                if not domains[neighbor]:
                    return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}, domains: Optional[Dict[V, List[D]]] = None) -> Optional[
        Dict[V, D]]:
        self.iterations += 1  # Count each call to backtracking_search as an iteration

        if len(assignment) == len(self.variables):
            return assignment

        if domains is None:
            domains = copy.deepcopy(self.domains)

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            local_assignment = assignment.copy()
            local_assignment[variable] = value
            if self.consistent(variable, local_assignment):
                local_domains = copy.deepcopy(domains)
                if self.forward_checking(variable, value, local_assignment, local_domains):
                    result = self.backtracking_search(local_assignment, local_domains)
                    if result is not None:
                        return result
        self.failures += 1  # Count each time backtracking occurs
        return None


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]


if __name__ == "__main__":
    variables: List[str] = [
        "Volyn", "Rivne", "Zhytomyr", "Chernihiv", "Sumy",
        "Lviv", "Ternopil", "Khmelnytskyi", "Vinnytsia", "Kiev",
        "Zakarpattia", "Ivano-Frankivsk", "Chernivtsi", "Cherkasy", "Poltava",
        "Kharkiv", "Donetsk", "Luhansk", "Dnipropetrovsk", "Zaporizhzhia",
        "Mykolaiv", "Kherson", "Odessa", "Kirovohrad", "Crimea"
    ]

    domains: Dict[str, List[str]] = {variable: ["red", "green", "blue", "yellow"] for variable in variables}

    neighbors = [
        ('Volyn', 'Rivne'), ('Volyn', 'Lviv'), ('Lviv', 'Zakarpattia'), ('Lviv', 'Ternopil'),
        ('Lviv', 'Ivano-Frankivsk'), ('Ivano-Frankivsk', 'Ternopil'), ('Ivano-Frankivsk', 'Chernivtsi'),
        ('Ivano-Frankivsk', 'Zakarpattia'), ('Ternopil', 'Rivne'), ('Ternopil', 'Khmelnytskyi'),
        ('Chernivtsi', 'Ternopil'), ('Khmelnytskyi', 'Vinnytsia'), ('Khmelnytskyi', 'Chernivtsi'),
        ('Rivne', 'Zhytomyr'), ('Rivne', 'Khmelnytskyi'), ('Zhytomyr', 'Khmelnytskyi'), ('Zhytomyr', 'Kiev'),
        ('Zhytomyr', 'Vinnytsia'), ('Vinnytsia', 'Kiev'), ('Vinnytsia', 'Chernivtsi'), ('Vinnytsia', 'Cherkasy'),
        ('Vinnytsia', 'Odessa'), ('Vinnytsia', 'Kirovohrad'), ('Kiev', 'Cherkasy'), ('Cherkasy', 'Kirovohrad'),
        ('Cherkasy', 'Poltava'), ('Poltava', 'Kiev'), ('Poltava', 'Kharkiv'), ('Poltava', 'Sumy'),
        ('Kiev', 'Chernihiv'),
        ('Kirovohrad', 'Mykolaiv'), ('Kirovohrad', 'Odessa'), ('Kirovohrad', 'Dnipropetrovsk'), ('Odessa', 'Mykolaiv'),
        ('Mykolaiv', 'Kherson'), ('Kherson', 'Zaporizhzhia'), ('Zaporizhzhia', 'Dnipropetrovsk'),
        ('Dnipropetrovsk', 'Kharkiv'),
        ('Kirovohrad', 'Poltava'), ('Poltava', 'Dnipropetrovsk'), ('Kharkiv', 'Sumy'), ('Kharkiv', 'Luhansk'),
        ('Kharkiv', 'Donetsk'),
        ('Zaporizhzhia', 'Donetsk'), ('Donetsk', 'Luhansk'), ('Sumy', 'Chernihiv'), ('Mykolaiv', 'Dnipropetrovsk'),
        ('Dnipropetrovsk', 'Donetsk'), ('Poltava', 'Chernihiv'), ('Kherson', 'Crimea'), ('Rivne', 'Lviv'),
        ('Kherson', 'Dnipropetrovsk'),
    ]

    # Using CSP with BT+MCV+LCV+FC
    csp: CSP[str, str] = CSP(variables, domains)
    for place1, place2 in neighbors:
        csp.add_constraint(MapColoringConstraint(place1, place2))

    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found with BT+MCV+LCV+FC!")
    else:
        print("Solution found with BT+MCV+LCV+FC!")
        print(solution)

    print(f"Iterations with BT+MCV+LCV+FC: {csp.iterations}")
    print(f"Failures with BT+MCV+LCV+FC: {csp.failures}")

    # Using CSP with BT+MCV

    file_path = 'UA_FULL_Ukraine.geojson'
    gdf = gpd.read_file(file_path)

    # Map the solution to the regions for BT+MCV+LCV+FC
    region_name_mapping = {
        "Volyn": "Волинська область",
        "Rivne": "Рівненська область",
        "Zhytomyr": "Житомирська область",
        "Chernihiv": "Чернігівська область",
        "Sumy": "Сумська область",
        "Lviv": "Львівська область",
        "Ternopil": "Тернопільська область",
        "Khmelnytskyi": "Хмельницька область",
        "Vinnytsia": "Вінницька область",
        "Kiev": "Київська область",
        "Zakarpattia": "Закарпатська область",
        "Ivano-Frankivsk": "Івано-Франківська область",
        "Chernivtsi": "Чернівецька область",
        "Cherkasy": "Черкаська область",
        "Poltava": "Полтавська область",
        "Kharkiv": "Харківська область",
        "Donetsk": "Донецька область",
        "Luhansk": "Луганська область",
        "Dnipropetrovsk": "Дніпропетровська область",
        "Zaporizhzhia": "Запорізька область",
        "Mykolaiv": "Миколаївська область",
        "Kherson": "Херсонська область",
        "Odessa": "Одеська область",
        "Kirovohrad": "Кіровоградська область",
        "Crimea": "Автономна Республіка Крим"
    }

    gdf["color_bt_mcv_lcv_fc"] = gdf["name"].map({region_name_mapping[k]: v for k, v in solution.items()})

    fig, ax = plt.subplots(1, 3, figsize=(30, 10))
    gdf.boundary.plot(ax=ax[0], linewidth=1)
    gdf.plot(column="color_bt_mcv_lcv_fc", ax=ax[0], legend=True, legend_kwds={'bbox_to_anchor': (1, 1)})
    ax[0].set_title("BT+MCV+LCV+FC")

    # Plot the map for BT+MCV

    plt.show()
