public class Nodo {
    private String nombre;
    private Nodo nodoIzquierdo;
    private Nodo nodoDerecho;

    public Nodo (String nombre) {
        this.nombre = nombre;
        this.nodoIzquierdo = null;
        this.nodoDerecho = null;
    }

    public String getNombre() {
        return nombre;
    }
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    public Nodo getNodoIzquierdo() {
        return nodoIzquierdo;
    }
    public void setNodoIzquierdo(Nodo nodoIzquierdo) {
        this.nodoIzquierdo = nodoIzquierdo;
    }
    public Nodo getNodoDerecho() {
        return nodoDerecho;
    }
    public void setNodoDerecho(Nodo nodoDerecho) {
        this.nodoDerecho = nodoDerecho;
    }
    
}
