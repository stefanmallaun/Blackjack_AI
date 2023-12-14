from pybrain.optimization import PGPE
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import LinearLayer, FullConnection

def run(net, task):
    # Set up initial values
    old_state = task.reset()
    action = task.choose_action(old_state)
    action_int = task.action_to_int[action]

    while not task.check_winner(task.player_hand, task.dealer_hand):
        # Apply action
        reward = task.get_reward(task.player_hand, task.dealer_hand)
        new_state = task.get_state(task.player_hand, task.dealer_hand)

        # Update network weights
        output = net.activate([*old_state, action_int])
        net.adapt(output, reward)

        # Prepare for next iteration
        old_state = new_state
        action = task.choose_action(old_state)
        action_int = task.action_to_int[action]

    # Return final result
    return reward

# Create network
structure = [5]
net = buildNetwork(structure[0], 1, bias=False)
net.structure = FullConnection(net.inlinks, net.outlinks)

# Set up optimization task
optimizer = PGPE(
    network=net,
    population_size=100,
    learning_rate=0.01,
    errors="normalized",
    mutation_rate=0.01,
    elitism_replacement=False,
    n_top_performers=50,
    best_replacement=True,
    recurrent=False,
)

# Train network
for generation in range(100):
    optimizer.optimize()

# Run simulation
result = run(net, task)
print("Final Result:", result)