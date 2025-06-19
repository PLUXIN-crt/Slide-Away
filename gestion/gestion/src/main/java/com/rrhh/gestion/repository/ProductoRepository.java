package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductoRepository extends JpaRepository<Producto, Integer> {
    
    @Query("SELECT p FROM Producto p JOIN FETCH p.categoria JOIN FETCH p.marca JOIN FETCH p.proveedor WHERE p.nombre LIKE %:nombre%")
    List<Producto> findByNombreContainingIgnoreCase(@Param("nombre") String nombre);
    
    @Query("SELECT p FROM Producto p JOIN FETCH p.categoria JOIN FETCH p.marca JOIN FETCH p.proveedor WHERE p.categoria.id = :categoriaId")
    List<Producto> findByCategoriaId(@Param("categoriaId") Integer categoriaId);
    
    @Query("SELECT p FROM Producto p JOIN FETCH p.categoria JOIN FETCH p.marca JOIN FETCH p.proveedor WHERE p.marca.id = :marcaId")
    List<Producto> findByMarcaId(@Param("marcaId") Integer marcaId);
}
