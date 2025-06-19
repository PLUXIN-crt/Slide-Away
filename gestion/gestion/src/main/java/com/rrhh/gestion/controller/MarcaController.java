package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Marca;
import com.rrhh.gestion.repository.MarcaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/marcas")
@CrossOrigin(origins = "*")
public class MarcaController {

    @Autowired
    private MarcaRepository marcaRepository;

    // Obtener todas las marcas
    @GetMapping
    public ResponseEntity<List<Marca>> getAllMarcas() {
        List<Marca> marcas = marcaRepository.findAll();
        return ResponseEntity.ok(marcas);
    }

    // Buscar marca por ID
    @GetMapping("/{id}")
    public ResponseEntity<Marca> getMarcaById(@PathVariable Integer id) {
        Optional<Marca> marca = marcaRepository.findById(id);
        if (marca.isPresent()) {
            return ResponseEntity.ok(marca.get());
        }
        return ResponseEntity.notFound().build();
    }
}