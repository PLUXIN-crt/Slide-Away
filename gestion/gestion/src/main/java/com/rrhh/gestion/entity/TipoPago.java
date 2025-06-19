package com.rrhh.gestion.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "tipo_pago")
public class TipoPago {
    @Id
    @Column(name = "id_tipo_pago")
    private Integer idTipoPago;
    
    @Column(nullable = false, length = 30)
    private String nombre;
    
    @Column(length = 100)
    private String descripcion;
    
    // Constructors
    public TipoPago() {}
    
    // Getters and Setters
    public Integer getIdTipoPago() { return idTipoPago; }
    public void setIdTipoPago(Integer idTipoPago) { this.idTipoPago = idTipoPago; }
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
}
