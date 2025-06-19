package com.rrhh.gestion.dto;

public class ClienteDTO {
    private String rut;
    private String nombre;
    private String apellidos;
    private String telefono;
    private String correo;
    private Integer idComuna;
    private String nombreComuna;
    
    // Constructors
    public ClienteDTO() {}
    
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
    
    public Integer getIdComuna() { return idComuna; }
    public void setIdComuna(Integer idComuna) { this.idComuna = idComuna; }
    
    public String getNombreComuna() { return nombreComuna; }
    public void setNombreComuna(String nombreComuna) { this.nombreComuna = nombreComuna; }
}
