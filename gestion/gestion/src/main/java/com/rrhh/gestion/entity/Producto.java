package com.rrhh.gestion.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name="producto")
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private String nombre;
    private String descripcion;
    private int stock;
    private BigDecimal precio;

    @ManyToOne
    @JoinColumn(name="categoria_id", nullable = false)
    @JsonIgnoreProperties("productos")
    private Categoria categoria;

    @ManyToOne
    @JoinColumn(name="marca_id", nullable = false)
    @JsonIgnoreProperties("productos")
    private Marca marca;

    @ManyToOne
    @JoinColumn(name="proveedor_id", nullable = false)
    @JsonIgnoreProperties("productos")
    private Proveedor proveedor;

    public Producto() {}

    public Producto(String nombre, String descripcion, int stock, BigDecimal precio,
                    Categoria categoria, Marca marca, Proveedor proveedor) {
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.stock = stock;
        this.precio = precio;
        this.categoria = categoria;
        this.marca = marca;
        this.proveedor = proveedor;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    public int getStock() { return stock; }
    public void setStock(int stock) { this.stock = stock; }
    public BigDecimal getPrecio() { return precio; }
    public void setPrecio(BigDecimal precio) { this.precio = precio; }
    public Categoria getCategoria() { return categoria; }
    public void setCategoria(Categoria categoria) { this.categoria = categoria; }
    public Marca getMarca() { return marca; }
    public void setMarca(Marca marca) { this.marca = marca; }
    public Proveedor getProveedor() { return proveedor; }
    public void setProveedor(Proveedor proveedor) { this.proveedor = proveedor; }
}