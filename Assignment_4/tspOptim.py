# If running in a fresh environment, uncomment as needed:
# !pip -q install matplotlib
import math
import random
from dataclasses import dataclass
from typing import List, Tuple
import matplotlib.pyplot as plt

# =============================================================================
# Part 1 — TSP utilities (provided)
# =============================================================================

Point = Tuple[float, float]
Tour = List[int]

def make_cities(n: int = 40, seed: int = 7) -> List[Point]:
    # Reproducible 2D city coordinates in [0, 1]x[0, 1].
    rng = random.Random(seed)
    return [(rng.random(), rng.random()) for _ in range(n)]

def dist(a: Point, b: Point) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.hypot(dx, dy)

def tour_length(cities: List[Point], tour: Tour) -> float:
    # Total length of a closed tour.
    n = len(tour)
    total = 0.0
    for i in range(n):
        total += dist(cities[tour[i]], cities[tour[(i + 1) % n]])
    return total

def is_valid_tour(tour: Tour, n: int) -> bool:
    return len(tour) == n and set(tour) == set(range(n))

def random_tour(n: int, rng: random.Random) -> Tour:
    t = list(range(n))
    rng.shuffle(t)
    return t

def nearest_neighbor_tour(cities: List[Point], start: int = 0) -> Tour:
    # Deterministic baseline: greedy nearest neighbor.
    n = len(cities)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)
    cur = start
    while unvisited:
        nxt = min(unvisited, key=lambda j: dist(cities[cur], cities[j]))
        tour.append(nxt)
        unvisited.remove(nxt)
        cur = nxt
    return tour


# =============================================================================
# Part 2 — Neighborhood operator (2-opt) (provided)
# =============================================================================

def two_opt_swap(tour: Tour, i: int, k: int) -> Tour:
    # Return a new tour where the segment [i:k] is reversed.
    return tour[:i] + list(reversed(tour[i:k + 1])) + tour[k + 1:]

def random_two_opt_neighbor(tour: Tour, rng: random.Random) -> Tour:
    # Pick a random 2-opt move.
    n = len(tour)
    i = rng.randrange(0, n - 1)
    k = rng.randrange(i + 1, n)
    return two_opt_swap(tour, i, k)


# =============================================================================
# Part 3 — Visualization helpers (provided)
# =============================================================================

def plot_tour(cities: List[Point], tour: Tour, title: str = "") -> None:
    xs = [cities[i][0] for i in tour] + [cities[tour[0]][0]]
    ys = [cities[i][1] for i in tour] + [cities[tour[0]][1]]
    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, marker="o")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()

def plot_history(series: List[float], title: str, ylabel: str = "Value") -> None:
    plt.figure(figsize=(7, 4))
    plt.plot(series)
    plt.title(title)
    plt.xlabel("Iteration")
    plt.ylabel(ylabel)
    plt.show()

def plot_compare(sa_hist: List[float], ga_hist: List[float]) -> None:
    # Overlay histories (x-axis is not identical meaning; this is a visual comparison).
    plt.figure(figsize=(8, 4))
    plt.plot(sa_hist, label="SA best-so-far")
    plt.plot(
        [i * (len(sa_hist) / max(1, len(ga_hist) - 1)) for i in range(len(ga_hist))],
        ga_hist,
        label="GA best-by-gen"
    )
    plt.title("SA vs GA: Best tour length over time (scaled x-axis)")
    plt.xlabel("Progress (scaled)")
    plt.ylabel("Length")
    plt.legend()
    plt.show()


# =============================================================================
# Part 4 — Baseline tour (nearest neighbor) (provided)
# =============================================================================

cities = make_cities(n=40, seed=7)
nn_tour = nearest_neighbor_tour(cities, start=0)
nn_len = tour_length(cities, nn_tour)
print(f"Nearest-neighbor length: {nn_len:.4f}")
plot_tour(cities, nn_tour, title=f"Nearest Neighbor (L={nn_len:.4f})")


# =============================================================================
# Part 5A — Code Skeleton: Simulated Annealing (SA)
# =============================================================================

@dataclass
class SAConfig:
    iters: int = 20_000
    t0: float = 0.2
    alpha: float = 0.9995
    seed: int = 123
    report_every: int = 2000

def simulated_annealing_tsp(
    cities: List[Point], init_tour: Tour, cfg: SAConfig
) -> Tuple[Tour, float, List[float]]:
    rng = random.Random(cfg.seed)
    n = len(cities)
    assert is_valid_tour(init_tour, n), "init_tour must be a valid permutation"

    cur_tour = init_tour[:]
    cur_len = tour_length(cities, cur_tour)
    best_tour = cur_tour[:]
    best_len = cur_len
    history = [best_len]
    T = cfg.t0

    for it in range(cfg.iters):
        cand_tour = random_two_opt_neighbor(cur_tour, rng)
        cand_len = tour_length(cities, cand_tour)
        delta = cand_len - cur_len

        
        if delta <= 0:
            accept = True
        else:
            accept = rng.random() < math.exp(-delta / T)

        if accept:
            cur_tour, cur_len = cand_tour, cand_len
            if cur_len < best_len:
                best_tour, best_len = cur_tour[:], cur_len

        history.append(best_len)

        # TODO: cooling schedule
        # How is T adjusted?
        T = max(T * cfg.alpha, 0.00000001)

        if cfg.report_every and (it + 1) % cfg.report_every == 0:
            print(f"[SA] iter={it+1:6d} T={T:.4g} cur={cur_len:.4f} best={best_len:.4f}")

    return best_tour, best_len, history


# Run SA (after you implement it)
sa_cfg = SAConfig(iters=20_000, t0=0.2, alpha=0.9995, seed=123, report_every=2000)
sa_best_tour, sa_best_len, sa_hist = simulated_annealing_tsp(cities, nn_tour[:], sa_cfg)
print(f"SA best length: {sa_best_len:.4f}")
print(f"SA improvement vs NN: {(nn_len - sa_best_len) / nn_len * 100:.2f}%")
assert is_valid_tour(sa_best_tour, len(cities))
plot_tour(cities, sa_best_tour, title=f"SA Best (L={sa_best_len:.4f})")
plot_history(sa_hist, title="SA Best-so-far Length", ylabel="Length")


# =============================================================================
# Part 5B — Code Skeleton: Genetic Algorithm (GA) for TSP
# =============================================================================

@dataclass
class GAConfig:
    pop_size: int = 300
    generations: int = 800
    tournament_k: int = 5
    crossover_rate: float = 0.9
    mutation_rate: float = 0.3
    elite_size: int = 10
    seed: int = 999
    report_every: int = 100

def tournament_select(
    pop: List[Tour], lengths: List[float], k: int, rng: random.Random
) -> Tour:
    candidates = rng.sample(range(len(pop)), k)
    best = min(candidates, key = lambda i : lengths[i])
    return pop[best]
    # TODO: tournament selection (minimize length)
    

def order_crossover_ox(parent1: Tour, parent2: Tour, rng: random.Random) -> Tour:
    # TODO: order crossover (OX)
    n = len(parent1)
    i, j = sorted(rng.sample(range(n), 2))

    child = [-1] * n
    child[i:j+1] = parent1[i:j+1]
    remaining = [x for x in parent2 if x not in child]
    pos = 0
    for k in range(n):
        if child[k] == -1:
            child[k] = remaining[pos]
            pos += 1
    return child



def mutate_swap(tour: Tour, rng: random.Random) -> Tour:
    # TODO: swap mutation
    result = tour[:]
    i, j = rng.sample(range(len(tour)), 2)
    result[i] , result[j] = result[j], result[i]
    return result
    

def genetic_algorithm_tsp(
    cities: List[Point], init_seed_tours: List[Tour], cfg: GAConfig
) -> Tuple[Tour, float, List[float]]:
    rng = random.Random(cfg.seed)
    n = len(cities)

    pop: List[Tour] = []
    for t in init_seed_tours:
        assert is_valid_tour(t, n)
        pop.append(t[:])
    while len(pop) < cfg.pop_size:
        pop.append(random_tour(n, rng))

    lengths = [tour_length(cities, t) for t in pop]
    best_idx = min(range(len(pop)), key=lambda i: lengths[i])
    best_tour = pop[best_idx][:]
    best_len = lengths[best_idx]
    history = [best_len]

    for gen in range(cfg.generations):
        elite_indices = sorted(range(len(pop)), key=lambda i: lengths[i])[: cfg.elite_size]
        next_pop = [pop[i][:] for i in elite_indices]

        while len(next_pop) < cfg.pop_size:
            p1 = tournament_select(pop, lengths, cfg.tournament_k, rng)
            p2 = tournament_select(pop, lengths, cfg.tournament_k, rng)

            if rng.random() < cfg.crossover_rate:
                child = order_crossover_ox(p1, p2, rng)
            else:
                child = p1[:]

            if rng.random() < cfg.mutation_rate:
                child = mutate_swap(child, rng)

            next_pop.append(child)

        pop = next_pop
        lengths = [tour_length(cities, t) for t in pop]
        gen_best_idx = min(range(len(pop)), key=lambda i: lengths[i])
        gen_best_len = lengths[gen_best_idx]

        if gen_best_len < best_len:
            best_len = gen_best_len
            best_tour = pop[gen_best_idx][:]

        history.append(best_len)

        if cfg.report_every and (gen + 1) % cfg.report_every == 0:
            print(f"[GA] gen={gen+1:4d} best={best_len:.4f}")

    assert is_valid_tour(best_tour, n)
    return best_tour, best_len, history


# Run GA (after you implement TODOs above)
ga_cfg = GAConfig(
    pop_size=500, generations=1000, tournament_k=3,
    crossover_rate=0.9, mutation_rate=0.4, elite_size=10,
    seed=999, report_every=100
)
ga_best_tour, ga_best_len, ga_hist = genetic_algorithm_tsp(
    cities, init_seed_tours=[nn_tour], cfg=ga_cfg
)
print(f"GA best length: {ga_best_len:.4f}")
print(f"GA improvement vs NN: {(nn_len - ga_best_len) / nn_len * 100:.2f}%")
plot_tour(cities, ga_best_tour, title=f"GA Best (L={ga_best_len:.4f})")
plot_history(ga_hist, title="GA Best-by-generation Length", ylabel="Length")


# =============================================================================
# Part 6 — Data Collection, Visualization and Comparison
# =============================================================================

# After both SA and GA work, run:
# plot_compare(sa_hist, ga_hist)
# And print a quick summary:
# print(f"NN: {nn_len:.4f} | SA: {sa_best_len:.4f} | GA: {ga_best_len:.4f}")

# TODO
plot_compare(sa_hist, ga_hist)
print(f"NN: {nn_len:.4f} | SA: {sa_best_len:.4f} | GA: {ga_best_len:.4f}")



# =============================================================================
# Example of how to check your work
# =============================================================================

def grade_check(
    nn_len: float, method_len: float,
    min_improvement_pct: float = 10.0, label: str = "Method"
) -> None:
    improvement = (nn_len - method_len) / nn_len * 100.0
    print(f"{label} length: {method_len:.4f} | Improvement vs NN: {improvement:.2f}%")
    assert improvement >= min_improvement_pct, (
        f"{label} improvement {improvement:.2f}% is below required {min_improvement_pct:.2f}%"
    )
    print(f"✅ {label} passed improvement threshold!")

grade_check(nn_len, sa_best_len, label="SA")
grade_check(nn_len, ga_best_len, label="GA")

# =============================================================================
# Part 7: Optional Task
# =============================================================================
# Try different crossover and/or mutation operations in GA and see if you can
# improve the performance. Document your effort in this section.