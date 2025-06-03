package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface ProductoRepository extends JpaRepository<Producto, Integer> {
    List<Producto> findByCategoriaId(int categoriaId);
    List<Producto> findByMarcaId(int marcaId);
    List<Producto> findByProveedorId(int proveedorId);
    List<Producto> findByStockLessThan(int stock);

    @Query("SELECT p FROM Producto p WHERE p.nombre LIKE %:nombre%")
    List<Producto> findByNombreContaining(@Param("nombre") String nombre);
}