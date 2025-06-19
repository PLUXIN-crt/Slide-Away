package com.rrhh.gestion.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "sucursal")
public class Sucursal {
    @Id
    @Column(name = "id_sucursal")
    private Integer idSucursal;
    
    @Column(name = "nombre_sucursal", nullable = false, length = 50)
    private String nombreSucursal;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_comuna", nullable = false)
    private Comuna comuna;
    
    @Column(name = "rut_encargado", nullable = false, length = 15)
    private String rutEncargado;
    
    // Constructors
    public Sucursal() {}
    
    // Getters and Setters
    public Integer getIdSucursal() { return idSucursal; }
    public void setIdSucursal(Integer idSucursal) { this.idSucursal = idSucursal; }
    
    public String getNombreSucursal() { return nombreSucursal; }
    public void setNombreSucursal(String nombreSucursal) { this.nombreSucursal = nombreSucursal; }
    
    public Comuna getComuna() { return comuna; }
    public void setComuna(Comuna comuna) { this.comuna = comuna; }
    
    public String getRutEncargado() { return rutEncargado; }
    public void setRutEncargado(String rutEncargado) { this.rutEncargado = rutEncargado; }
}
