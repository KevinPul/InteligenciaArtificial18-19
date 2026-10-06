public class Node implements Comparable<Node> {
    private String state;
    private int depth;
    private Node parent;
    private int cost;

    public Node(String state, Node parent) {
        this.state = state;
        this.parent = parent;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public int getDepth() {
        return depth;
    }

    public void setDepth(int depth) {
        this.depth = depth;
    }

    public Node getParent() {
        return parent;
    }

    public void setParent(Node parent) {
        this.parent = parent;
    }

    public int getCost() {
        return cost;
    }

    public void setCost(int cost) {
        this.cost = cost;
    }

    @Override
    public int compareTo(Node otroNodo) {
        return Integer.compare(this.cost, otroNodo.getCost());
    }
}