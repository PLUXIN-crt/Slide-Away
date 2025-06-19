package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Cliente;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ClienteRepository extends JpaRepository<Cliente, String> {
    
    @Query("SELECT c FROM Cliente c JOIN FETCH c.comuna WHERE c.nombre LIKE %:nombre% OR c.apellidos LIKE %:apellidos%")
    List<Cliente> findByNombreOrApellidosContainingIgnoreCase(@Param("nombre") String nombre, @Param("apellidos") String apellidos);
    
    @Query("SELECT c FROM Cliente c JOIN FETCH c.comuna WHERE c.correo = :correo")
    Cliente findByCorreo(@Param("correo") String correo);
    
    @Query("SELECT c FROM Cliente c JOIN FETCH c.comuna WHERE c.comuna.id = :comunaId")
    List<Cliente> findByComunaId(@Param("comunaId") Integer comunaId);
}
