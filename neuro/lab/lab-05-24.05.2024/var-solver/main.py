import time
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

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        self.iterations += 1  # Count each call to backtracking_search as an iteration

        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        self.failures += 1  # Count each time backtracking occurs
        return None


class CSP_BT_MCV(CSP[V, D]):
    def select_unassigned_variable(self, assignment: Dict[V, D]) -> V:
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))


class CSP_BT_MCV_LCV_FC(CSP_BT_MCV[V, D]):
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


class Metrics:
    def __init__(self):
        self.iterations = []
        self.failures = []
        self.time = []

    def add(self, iterations, failures, time):
        self.iterations.append(iterations)
        self.failures.append(failures)
        self.time.append(time)


def plot_metrics(metrics, method_name):
    fig, ax = plt.subplots(3, 1, figsize=(10, 18))

    # Iterations
    ax[0].plot(range(4, 11), metrics.iterations, label=f'{method_name}')
    ax[0].set_title(f'Iterations - {method_name}')
    ax[0].set_xlabel('Number of Colors')
    ax[0].set_ylabel('Iterations')

    # Failures
    ax[1].plot(range(4, 11), metrics.failures, label=f'{method_name}')
    ax[1].set_title(f'Failures - {method_name}')
    ax[1].set_xlabel('Number of Colors')
    ax[1].set_ylabel('Failures')

    # Time
    ax[2].plot(range(4, 11), metrics.time, label=f'{method_name}')
    ax[2].set_title(f'Time - {method_name}')
    ax[2].set_xlabel('Number of Colors')
    ax[2].set_ylabel('Time (seconds)')

    plt.tight_layout()
    plt.show()


def plot_solution(gdf, solution, title):
    gdf["color"] = gdf["name"].map(solution)
    # Ensure that there are values to plot
    if not gdf["color"].isnull().all():
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        gdf.boundary.plot(ax=ax, linewidth=1)
        gdf.plot(column="color", ax=ax, legend=True, legend_kwds={'bbox_to_anchor': (1, 1)})
        ax.set_title(title)
        plt.tight_layout()
        plt.show()


def draw_map_with_4_colors():
    variables: List[str] = [
        "Volyn", "Rivne", "Zhytomyr", "Chernihiv", "Sumy",
        "Lviv", "Ternopil", "Khmelnytskyi", "Vinnytsia", "Kiev",
        "Zakarpattia", "Ivano-Frankivsk", "Chernivtsi", "Cherkasy", "Poltava",
        "Kharkiv", "Donetsk", "Luhansk", "Dnipropetrovsk", "Zaporizhzhia",
        "Mykolaiv", "Kherson", "Odessa", "Kirovohrad", "Crimea"
    ]

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

    domains: Dict[str, List[str]] = {variable: ["red", "green", "blue", "yellow"] for variable in variables}

    csp: CSP_BT_MCV_LCV_FC[str, str] = CSP_BT_MCV_LCV_FC(variables, domains)
    for place1, place2 in neighbors:
        csp.add_constraint(MapColoringConstraint(place1, place2))

    solution: Optional[Dict[str, str]] = csp.backtracking_search()

    if solution is not None:
        print("Solution found with 4 colors:")
        print(solution)

        file_path = 'UA_FULL_Ukraine.geojson'
        gdf = gpd.read_file(file_path)

        solution_map = {variable: solution.get(variable, "unknown") for variable in variables}
        plot_solution(gdf, solution_map, "4 Colors Solution")


if __name__ == "__main__":
    draw_map_with_4_colors()
    variables: List[str] = [
        "Volyn", "Rivne", "Zhytomyr", "Chernihiv", "Sumy",
        "Lviv", "Ternopil", "Khmelnytskyi", "Vinnytsia", "Kiev",
        "Zakarpattia", "Ivano-Frankivsk", "Chernivtsi", "Cherkasy", "Poltava",
        "Kharkiv", "Donetsk", "Luhansk", "Dnipropetrovsk", "Zaporizhzhia",
        "Mykolaiv", "Kherson", "Odessa", "Kirovohrad", "Crimea"
    ]

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

    colors = [f"color_{i}" for i in range(10)]

    metrics_bt_mcv_lcv_fc = Metrics()
    metrics_bt_mcv = Metrics()
    metrics_bt = Metrics()

    solutions_bt_mcv_lcv_fc = []
    solutions_bt_mcv = []
    solutions_bt = []

    for i in range(4, 11):
        current_colors = colors[:i]
        domains: Dict[str, List[str]] = {variable: current_colors for variable in variables}

        # Using CSP with BT+MCV+LCV+FC
        csp: CSP_BT_MCV_LCV_FC[str, str] = CSP_BT_MCV_LCV_FC(variables, domains)
        for place1, place2 in neighbors:
            csp.add_constraint(MapColoringConstraint(place1, place2))

        start_time = time.time()
        solution: Optional[Dict[str, str]] = csp.backtracking_search()
        end_time = time.time()

        if solution is not None:
            metrics_bt_mcv_lcv_fc.add(csp.iterations, csp.failures, end_time - start_time)
            solutions_bt_mcv_lcv_fc.append(solution)

        # Using CSP with BT+MCV
        csp_bt_mcv: CSP_BT_MCV[str, str] = CSP_BT_MCV(variables, domains)
        for place1, place2 in neighbors:
            csp_bt_mcv.add_constraint(MapColoringConstraint(place1, place2))

        start_time = time.time()
        solution_bt_mcv: Optional[Dict[str, str]] = csp_bt_mcv.backtracking_search()
        end_time = time.time()

        if solution_bt_mcv is not None:
            metrics_bt_mcv.add(csp_bt_mcv.iterations, csp_bt_mcv.failures, end_time - start_time)
            solutions_bt_mcv.append(solution_bt_mcv)

        # Using CSP with only BT
        csp_bt: CSP[str, str] = CSP(variables, domains)
        for place1, place2 in neighbors:
            csp_bt.add_constraint(MapColoringConstraint(place1, place2))

        start_time = time.time()
        solution_bt: Optional[Dict[str, str]] = csp_bt.backtracking_search()
        end_time = time.time()

        if solution_bt is not None:
            metrics_bt.add(csp_bt.iterations, csp_bt.failures, end_time - start_time)
            solutions_bt.append(solution_bt)

    plot_metrics(metrics_bt_mcv_lcv_fc, "BT+MCV+LCV+FC")
    plot_metrics(metrics_bt_mcv, "BT+MCV")
    plot_metrics(metrics_bt, "BT")

    # Plotting the map for the last iteration (10 colors)
    file_path = 'UA_FULL_Ukraine.geojson'
    gdf = gpd.read_file(file_path)

    if solutions_bt_mcv_lcv_fc:
        solution_map = {variable: solutions_bt_mcv_lcv_fc[-1].get(variable, "unknown") for variable in variables}
        plot_solution(gdf, solution_map, "BT+MCV+LCV+FC")

    if solutions_bt_mcv:
        solution_map = {variable: solutions_bt_mcv[-1].get(variable, "unknown") for variable in variables}
        plot_solution(gdf, solution_map, "BT+MCV")

    if solutions_bt:
        solution_map = {variable: solutions_bt[-1].get(variable, "unknown") for variable in variables}
        plot_solution(gdf, solution_map, "BT")
