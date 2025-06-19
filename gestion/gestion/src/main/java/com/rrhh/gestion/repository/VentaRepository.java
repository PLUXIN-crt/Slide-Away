package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Venta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface VentaRepository extends JpaRepository<Venta, Integer> {
    
    @Query("SELECT v FROM Venta v JOIN FETCH v.cliente JOIN FETCH v.tipoPago JOIN FETCH v.sucursal WHERE v.cliente.rut = :rutCliente")
    List<Venta> findByClienteRut(@Param("rutCliente") String rutCliente);
    
    @Query("SELECT v FROM Venta v JOIN FETCH v.cliente JOIN FETCH v.tipoPago JOIN FETCH v.sucursal WHERE v.fechaVenta BETWEEN :fechaInicio AND :fechaFin")
    List<Venta> findByFechaVentaBetween(@Param("fechaInicio") LocalDate fechaInicio, @Param("fechaFin") LocalDate fechaFin);
    
    @Query("SELECT v FROM Venta v JOIN FETCH v.cliente JOIN FETCH v.tipoPago JOIN FETCH v.sucursal WHERE v.sucursal.id = :sucursalId")
    List<Venta> findBySucursalId(@Param("sucursalId") Integer sucursalId);
}
