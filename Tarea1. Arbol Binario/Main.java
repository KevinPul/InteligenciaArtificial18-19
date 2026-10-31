public class Main {
    public static void main(String[] args) {
        Nodo raiz = new Nodo("M");
        Nodo nodoIzq = new Nodo("A");
        Nodo nodoDer = new Nodo("Z");

        raiz.setNodoIzquierdo(nodoIzq); 
        raiz.setNodoDerecho(nodoDer);

        Arbol arbol = new Arbol(raiz);

        System.out.println(arbol.vacio());
        
        Nodo resultado = arbol.buscarNodo("Z");
        if (resultado != null) {
            System.out.println(resultado.getNombre());
        }
    }

}
