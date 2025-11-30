import random
import time
import matplotlib.pyplot as plt
from rbt_logic import RedBlackTree          # ← only change


def measure_insert_time(n):
    """Measures how long it takes to insert n random nodes into a Red-Black tree."""
    rbt = RedBlackTree(color_only=False)    # full rotations
    nums = random.sample(range(n * 10), n)

    start = time.time()
    for num in nums:
        rbt.insert(num)
    rbt.rebalance_all()                     # finish any pending fixes
    end = time.time()

    return end - start


# --- same node counts you used for BST ---
sizes = [10000, 20000, 30000, 50000, 60000]

times = []
for n in sizes:
    t = measure_insert_time(n)
    times.append(t)
    print(f"{n} nodes → {t:.6f} seconds")

# --- plot the line chart ---
plt.figure()
plt.plot(sizes, times, marker='o', color='#3b82f6')
plt.title("Red-Black Tree Insertion Line Chart")
plt.xlabel("Total Input Nodes")
plt.ylabel("Total Time (seconds)")
plt.grid(True)
plt.tight_layout()

plt.savefig("rbt_chart.png")
plt.show()
