package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Marca;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MarcaRepository extends JpaRepository<Marca, Integer> {
}