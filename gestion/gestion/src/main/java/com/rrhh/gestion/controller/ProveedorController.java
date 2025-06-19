package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Proveedor;
import com.rrhh.gestion.repository.ProveedorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/proveedores")
@CrossOrigin(origins = "*")
public class ProveedorController {

    @Autowired
    private ProveedorRepository proveedorRepository;

    // Obtener todos los proveedores
    @GetMapping
    public ResponseEntity<List<Proveedor>> getAllProveedores() {
        List<Proveedor> proveedores = proveedorRepository.findAll();
        return ResponseEntity.ok(proveedores);
    }

    // Buscar proveedor por ID
    @GetMapping("/{id}")
    public ResponseEntity<Proveedor> getProveedorById(@PathVariable Integer id) {
        Optional<Proveedor> proveedor = proveedorRepository.findById(id);
        if (proveedor.isPresent()) {
            return ResponseEntity.ok(proveedor.get());
        }
        return ResponseEntity.notFound().build();
    }
}