package com.rrhh.gestion.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "comuna")
public class Comuna {
    @Id
    private Integer id;
    
    @Column(nullable = false, length = 30)
    private String nombre;
    
    // Constructors
    public Comuna() {}
    
    public Comuna(Integer id, String nombre) {
        this.id = id;
        this.nombre = nombre;
    }
    
    // Getters and Setters
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
}
