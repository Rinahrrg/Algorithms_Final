import random
import time
import matplotlib.pyplot as plt
from bst_logic import BinarySearchTree 

def measure_insert_time(n):
    """Measures how long it takes to insert n random nodes into BST."""
    bst = BinarySearchTree()
    nums = random.sample(range(n * 10), n)

    start = time.time()
    for num in nums:
        bst.insert(num)
    end = time.time()

    return end - start


#Node sizes
sizes = [10000, 20000, 30000, 50000, 60000]

times = []
for n in sizes:
    t = measure_insert_time(n)
    times.append(t)
    print(f"{n} nodes → {t:.6f} seconds")

#Plot the chart
plt.figure()
plt.plot(sizes, times, marker='o')
plt.title("Improved BST Algorithm Line Chart")
plt.xlabel("Total Input Nodes")
plt.ylabel("Total Time (seconds)")
plt.grid(True)
plt.tight_layout()

plt.savefig("bst_chart.png")   
plt.show()
