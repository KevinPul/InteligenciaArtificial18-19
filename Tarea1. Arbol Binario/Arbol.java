public class Arbol {
    private Nodo raiz;

    public Arbol() {
        this.raiz = null;
    }

    public Arbol(Nodo raiz) {
        this.raiz = raiz;
    }

    public boolean vacio() {
        return raiz == null;
    }

    public Nodo buscarNodo(String nombre) {
        Nodo actual = raiz;
        
        while (actual != null) {
            if (actual.getNombre().equals(nombre)) {
                return actual;
            }
            
            if (nombre.compareTo(actual.getNombre()) < 0) {
                actual = actual.getNodoIzquierdo();
            }
            else {
                actual = actual.getNodoDerecho();
            }
        }
        
        return null;
    }
}