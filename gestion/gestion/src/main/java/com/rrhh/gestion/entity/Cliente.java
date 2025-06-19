package com.rrhh.gestion.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "cliente")
public class Cliente {
    @Id
    @Column(length = 12)
    private String rut;
    
    @Column(nullable = false, length = 30, unique = true)
    private String nombre;
    
    @Column(nullable = false, length = 30, unique = true)
    private String apellidos;
    
    @Column(nullable = false, length = 30)
    private String telefono;
    
    @Column(nullable = false, length = 30)
    private String correo;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_comuna", nullable = false)
    private Comuna comuna;
    
    // Constructors
    public Cliente() {}
    
    // Getters and Setters
    public String getRut() { return rut; }
    public void setRut(String rut) { this.rut = rut; }
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
    public String getApellidos() { return apellidos; }
    public void setApellidos(String apellidos) { this.apellidos = apellidos; }
    
    public String getTelefono() { return telefono; }
    public void setTelefono(String telefono) { this.telefono = telefono; }
    
    public String getCorreo() { return correo; }
    public void setCorreo(String correo) { this.correo = correo; }
    
    public Comuna getComuna() { return comuna; }
    public void setComuna(Comuna comuna) { this.comuna = comuna; }
}
