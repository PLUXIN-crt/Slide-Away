package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Marca;
import com.rrhh.gestion.repository.MarcaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/marcas")
public class MarcaController {

    @Autowired
    private MarcaRepository marcaRepository;

    @GetMapping
    public List<Marca> obtenerMarcas() {
        return marcaRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Marca> obtenerMarca(@PathVariable int id) {
        Optional<Marca> marca = marcaRepository.findById(id);
        return marca.map(m -> ResponseEntity.ok(m))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Marca> crearMarca(@RequestBody Marca marca) {
        Marca nueva = marcaRepository.save(marca);
        return new ResponseEntity<>(nueva, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Marca> actualizarMarca(@PathVariable int id, @RequestBody Marca marca) {
        return marcaRepository.findById(id)
                .map(m -> {
                    m.setNombre(marca.getNombre());
                    return ResponseEntity.ok(marcaRepository.save(m));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarMarca(@PathVariable int id) {
        return marcaRepository.findById(id)
                .map(m -> {
                    marcaRepository.delete(m);
                    return ResponseEntity.ok().<Void>build();
                })
                .orElse(ResponseEntity.notFound().build());
    }
}