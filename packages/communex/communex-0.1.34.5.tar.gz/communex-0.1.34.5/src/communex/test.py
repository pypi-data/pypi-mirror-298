from communex.client import CommuneClient
from time import sleep
from communex._common import get_node_url
import concurrent.futures

node = get_node_url(use_testnet=True)
print(node)


def attack():
    print("#########################")
    print("trying to connect to node")
    x = CommuneClient(node)
    block = x.get_block()
    print(f"block: {block}")
    print("established connection")
    print("-------------------------")
    sleep(2)


def run_parallel_attacks(num_attacks):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(attack) for _ in range(num_attacks)]
    concurrent.futures.wait(futures)

if __name__ == "__main__":
    num_attacks = 100_000  # Specify the number of parallel attacks
    run_parallel_attacks(num_attacks)
