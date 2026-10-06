import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.Stack;
import java.util.PriorityQueue;

public class Tree {
    Node root;
    String initialState;
    String goalState;

    public Tree(String initialState, String goalState) {
        this.root = new Node(initialState, null);
        this.initialState = initialState;
        this.goalState = goalState;
    }
    // 1. Primero en anchura
    public void breadthFirstSearch() {
        long startTime = System.currentTimeMillis();
        Set<String> visited = new HashSet<String>();
        Node currentNode = root;
        Queue<Node> queue = new LinkedList<>();
        queue.add(currentNode);
        visited.add(currentNode.getState());

        while (!queue.isEmpty()) {
            currentNode = queue.poll();
            if(currentNode.getState().equals(goalState)) {
                long endTime = System.currentTimeMillis();
                System.out.println("RESULTADOS PRIMERO EN ANCHURA");
                System.out.println("Goal state found: " + currentNode.getState());
                System.out.println("Tiempo requerido: " + (endTime - startTime) + " ms");
                System.out.println("Nodos visitados (Espacio): " + visited.size());
                printPath(currentNode);
                return;
            }

            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState())) {
                    queue.add(child);
                }
            }
        }
        System.out.println("No se encontró solución con primero en anchura.");
    }
    // 2. Costo Uniforme
    public void uniformCostSearch() {
        long startTime = System.currentTimeMillis();
        Set<String> visited = new HashSet<>();
        PriorityQueue<Node> queue = new PriorityQueue<>();

        root.setCost(0);
        queue.add(root);

        while(!queue.isEmpty()) {
            Node currentNode = queue.poll();
            if(visited.contains(currentNode.getState())) {
                continue;
            }
            visited.add(currentNode.getState());

            if(currentNode.getState().equals(goalState)) {
                long endTime = System.currentTimeMillis();
                System.out.println("RESULTADOS COSTO UNIFORME");
                System.out.println("Meta encontrada: " + goalState);
                System.out.println("Tiempo requerido: " + (endTime - startTime) + "ms");
                System.out.println("Nodos visitados: " + visited.size());
                printPath(currentNode);
                return;
            }

            List<Node> children = NodeUtils.generateChildren(currentNode);
            for(Node child: children) {
                if(!visited.contains(child.getState())) {
                    child.setCost(currentNode.getCost() + 1);
                    queue.add(child);
                }
            }
        }
        System.out.println("No se encontró solucion con Costo Uniforme");
    }
    // 3. Primero en profundidad
    public void depthFirstSearch() {
        long startTime = System.currentTimeMillis();
        Set<String> visited = new HashSet<>();
        
        Stack<Node> stack = new Stack<>();
        
        stack.push(root);

        while (!stack.isEmpty()) {
            Node currentNode = stack.pop();

            if (visited.contains(currentNode.getState())) {
                continue;
            }
            visited.add(currentNode.getState());

            if (currentNode.getState().equals(goalState)) {
                long endTime = System.currentTimeMillis();
                System.out.println("----- RESULTADOS PRIMERO EN PROFUNDIDAD (DFS) -----");
                System.out.println("Meta encontrada: " + currentNode.getState());
                System.out.println("Tiempo requerido: " + (endTime - startTime) + " ms");
                System.out.println("Nodos visitados (Espacio): " + visited.size());
                printPath(currentNode);
                return;
            }

            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState())) {
                    stack.push(child);
                }
            }
        }
    System.out.println("No se encontró solución con Primero en Profundidad.");
    }

    // 4. Profundidad Limitada
    public Node depthLimitedSearch(int limit, boolean showLogs) {
        long startTime = System.currentTimeMillis();
        Set<String> visited = new HashSet<>();
        Stack<Node> stack = new Stack<>();
        
        root.setDepth(0);
        stack.push(root);

        while (!stack.isEmpty()) {
            Node currentNode = stack.pop();

            if (currentNode.getState().equals(goalState)) {
                if (showLogs) {
                    long endTime = System.currentTimeMillis();
                    System.out.println("----- RESULTADOS PROFUNDIDAD LIMITADA (Límite " + limit + ") -----");
                    System.out.println("Meta encontrada: " + currentNode.getState());
                    System.out.println("Tiempo requerido: " + (endTime - startTime) + " ms");
                    System.out.println("Nodos visitados (Espacio): " + visited.size());
                    printPath(currentNode);
                }
                return currentNode;
            }

            visited.add(currentNode.getState());

            if (currentNode.getDepth() < limit) {
                List<Node> children = NodeUtils.generateChildren(currentNode);
                for (Node child : children) {
                    if (!visited.contains(child.getState())) {
                        child.setDepth(currentNode.getDepth() + 1);
                        stack.push(child);
                    }
                }
            }
        }
        
        if (showLogs) {
            System.out.println("No se encontró solución con Profundidad Limitada en el límite " + limit);
        }
        return null;
    }

    // 5. Profundidad Iterativa
    public void iterativeDeepeningSearch(int maxDepth) {
        System.out.println("----- INICIANDO PROFUNDIDAD ITERATIVA (IDS) -----");
        long startTime = System.currentTimeMillis();
        
        for (int limit = 0; limit <= maxDepth; limit++) {
            Node result = depthLimitedSearch(limit, false);
            
            if (result != null) {
                long endTime = System.currentTimeMillis();
                System.out.println("¡Solución encontrada por IDS en el límite de profundidad: " + limit + "!");
                System.out.println("Tiempo total de todas las iteraciones: " + (endTime - startTime) + " ms");
                printPath(result);
                return;
            }
        }
        System.out.println("No se encontró solución con IDS tras alcanzar el límite máximo de " + maxDepth);
    }

    // 6. Bidireccional
    public void bidirectionalSearch() {
        long startTime = System.currentTimeMillis();

        Queue<Node> forwardQueue = new LinkedList<>();
        Queue<Node> backwardQueue = new LinkedList<>();

        Map<String, Node> forwardVisited = new HashMap<>();
        Map<String, Node> backwardVisited = new HashMap<>();

        forwardQueue.add(root);
        forwardVisited.put(root.getState(), root);

        Node goalNode = new Node(goalState, null);
        backwardQueue.add(goalNode);
        backwardVisited.put(goalState, goalNode);

        while (!forwardQueue.isEmpty() && !backwardQueue.isEmpty()) {
            
            Node currentForward = forwardQueue.poll();
            
            if (backwardVisited.containsKey(currentForward.getState())) {
                imprimirResultadosBidireccional(startTime, forwardVisited, backwardVisited, 
                        currentForward, backwardVisited.get(currentForward.getState()));
                return;
            }

            for (Node child : NodeUtils.generateChildren(currentForward)) {
                if (!forwardVisited.containsKey(child.getState())) {
                    forwardVisited.put(child.getState(), child);
                    forwardQueue.add(child);
                }
            }

            Node currentBackward = backwardQueue.poll();

            if (forwardVisited.containsKey(currentBackward.getState())) {
                imprimirResultadosBidireccional(startTime, forwardVisited, backwardVisited, 
                        forwardVisited.get(currentBackward.getState()), currentBackward);
                return;
            }

            for (Node child : NodeUtils.generateChildren(currentBackward)) {
                if (!backwardVisited.containsKey(child.getState())) {
                    backwardVisited.put(child.getState(), child);
                    backwardQueue.add(child);
                }
            }
        }
        System.out.println("No se encontró solución con Búsqueda Bidireccional.");
    }

    // Imprimir Resultados
    private void imprimirResultadosBidireccional(long startTime, Map<String, Node> fVis, Map<String, Node> bVis, Node fIntersect, Node bIntersect) {
        long endTime = System.currentTimeMillis();
        System.out.println("----- RESULTADOS BIDIRECCIONAL -----");
        System.out.println("Intersección encontrada en:\n" + NodeUtils.formatState(fIntersect.getState()));
        System.out.println("Tiempo requerido: " + (endTime - startTime) + " ms");
        System.out.println("Nodos visitados totales (Espacio): " + (fVis.size() + bVis.size()));

        LinkedList<String> path = new LinkedList<>();
        
        Node current = fIntersect;
        while (current != null) {
            path.addFirst(current.getState());
            current = current.getParent();
        }
        
        current = bIntersect.getParent();
        while (current != null) {
            path.addLast(current.getState());
            current = current.getParent();
        }

        System.out.println("Pasos para resolver (" + (path.size() - 1) + " movimientos):");
        for (String state : path) {
            System.out.print(NodeUtils.formatState(state));
            System.out.println("---");
        }
        System.out.println();
    }


    // Imprimir el camino
    private void printPath(Node goalNode) {
        LinkedList<String> path = new LinkedList<>();
        Node current = goalNode;

        while (current != null) {
            path.addFirst(current.getState());
            current = current.getParent(); 
        }

        System.out.println("Pasos para resolver (" + (path.size() - 1) + " movimientos):");
        for (String state : path) {
            System.out.println(NodeUtils.formatState(state));
            System.out.println("---");
        }
        System.out.println();
    }
}