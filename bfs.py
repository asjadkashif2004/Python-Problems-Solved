from collections import deque

def bfs(graph, start):
    # Create a queue for BFS and a set to track visited nodes
    queue = deque([start])
    visited = set([start])

    while queue:
        # Dequeue a node from the front of the queue
        node = queue.popleft()
        print(node, end=" ")  # Process the node (you can replace this with any operation)

        # Get all adjacent nodes (neighbors) of the dequeued node
        for neighbor in graph[node]:
            if neighbor not in visited:
                # Enqueue unvisited neighbors and mark them as visited
                queue.append(neighbor)
                visited.add(neighbor)

# Example usage:
# Graph represented as an adjacency list (dictionary)
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# Perform BFS starting from node 'A'
bfs(graph, 'A')
