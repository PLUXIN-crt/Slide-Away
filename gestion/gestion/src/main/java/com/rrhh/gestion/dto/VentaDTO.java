package com.rrhh.gestion.dto;

import java.math.BigDecimal;
import java.time.LocalDate;

public class VentaDTO {
    private Integer numeroDocumento;
    private String tipoDocumento;
    private LocalDate fechaVenta;
    private BigDecimal totalVenta;
    private Integer idTipoPago;
    private String nombreTipoPago;
    private String rutCliente;
    private String nombreCliente;
    private String apellidoCliente;
    private Integer idSucursal;
    private String nombreSucursal;
    
    // Constructors
    public VentaDTO() {}
    
    // Getters and Setters
    public Integer getNumeroDocumento() { return numeroDocumento; }
    public void setNumeroDocumento(Integer numeroDocumento) { this.numeroDocumento = numeroDocumento; }
    
    public String getTipoDocumento() { return tipoDocumento; }
    public void setTipoDocumento(String tipoDocumento) { this.tipoDocumento = tipoDocumento; }
    
    public LocalDate getFechaVenta() { return fechaVenta; }
    public void setFechaVenta(LocalDate fechaVenta) { this.fechaVenta = fechaVenta; }
    
    public BigDecimal getTotalVenta() { return totalVenta; }
    public void setTotalVenta(BigDecimal totalVenta) { this.totalVenta = totalVenta; }
    
    public Integer getIdTipoPago() { return idTipoPago; }
    public void setIdTipoPago(Integer idTipoPago) { this.idTipoPago = idTipoPago; }
    
    public String getNombreTipoPago() { return nombreTipoPago; }
    public void setNombreTipoPago(String nombreTipoPago) { this.nombreTipoPago = nombreTipoPago; }
    
    public String getRutCliente() { return rutCliente; }
    public void setRutCliente(String rutCliente) { this.rutCliente = rutCliente; }
    
    public String getNombreCliente() { return nombreCliente; }
    public void setNombreCliente(String nombreCliente) { this.nombreCliente = nombreCliente; }
    
    public String getApellidoCliente() { return apellidoCliente; }
    public void setApellidoCliente(String apellidoCliente) { this.apellidoCliente = apellidoCliente; }
    
    public Integer getIdSucursal() { return idSucursal; }
    public void setIdSucursal(Integer idSucursal) { this.idSucursal = idSucursal; }
    
    public String getNombreSucursal() { return nombreSucursal; }
    public void setNombreSucursal(String nombreSucursal) { this.nombreSucursal = nombreSucursal; }
}
