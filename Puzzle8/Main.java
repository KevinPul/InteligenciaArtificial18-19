public class Main {
    public static void main(String[] args) {
        String initialState = "13 425786"; 
        String goalState = "12345678 ";

        Tree tree = new Tree(initialState, goalState);
        
        System.out.println("=================================");
        tree.breadthFirstSearch();
        System.out.println("=================================");
        tree.uniformCostSearch();
        System.out.println("=================================");
        tree.depthFirstSearch();
        System.out.println("=================================");
        tree.depthLimitedSearch(15, true); 
        System.out.println("=================================");
        tree.iterativeDeepeningSearch(15);
        System.out.println("=================================");
        tree.bidirectionalSearch();
    }
}