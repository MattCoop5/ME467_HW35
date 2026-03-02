from hazardous_warehouse_env import HazardousWarehouseEnv
from hazardous_warehouse_viz import configure_rn_example_layout, replay_episode
from warehouse_z3_agent import WarehouseZ3Agent

env = HazardousWarehouseEnv(seed=0)
configure_rn_example_layout(env)
print("True state (hidden from agent):")
print(env.render(reveal=True))
agent = WarehouseZ3Agent(env)
agent.run(verbose=True)

print("\nReplaying KB agent episode (press SPACE to pause, arrows to step)...")
replay_episode(env.history, env, interval_ms=400)
