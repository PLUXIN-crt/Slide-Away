package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Producto;
import com.rrhh.gestion.repository.ProductoRepository;
import com.rrhh.gestion.dto.ProductoDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/productos")
public class ProductoController {

    @Autowired
    private ProductoRepository productoRepository;

    @GetMapping
    public List<Producto> obtenerProductos() {
        return productoRepository.findAll();
    }

    @GetMapping("/dto")
    public List<ProductoDTO> obtenerProductosDTO() {
        List<Producto> productos = productoRepository.findAll();
        List<ProductoDTO> productosDTO = new ArrayList<>();
        for (Producto p : productos) {
            productosDTO.add(new ProductoDTO(
                    p.getId(), p.getNombre(), p.getDescripcion(),
                    p.getStock(), p.getPrecio(),
                    p.getCategoria().getNombre(),
                    p.getMarca().getNombre(),
                    p.getProveedor().getNombre()
            ));
        }
        return productosDTO;
    }

    @GetMapping("/{id}")
    public ResponseEntity<Producto> obtenerProducto(@PathVariable int id) {
        Optional<Producto> producto = productoRepository.findById(id);
        return producto.map(p -> ResponseEntity.ok(p))
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/categoria/{categoriaId}")
    public List<Producto> obtenerProductosPorCategoria(@PathVariable int categoriaId) {
        return productoRepository.findByCategoriaId(categoriaId);
    }

    @GetMapping("/marca/{marcaId}")
    public List<Producto> obtenerProductosPorMarca(@PathVariable int marcaId) {
        return productoRepository.findByMarcaId(marcaId);
    }

    @GetMapping("/proveedor/{proveedorId}")
    public List<Producto> obtenerProductosPorProveedor(@PathVariable int proveedorId) {
        return productoRepository.findByProveedorId(proveedorId);
    }

    @GetMapping("/stock-bajo/{limite}")
    public List<Producto> obtenerProductosConStockBajo(@PathVariable int limite) {
        return productoRepository.findByStockLessThan(limite);
    }

    @GetMapping("/buscar")
    public List<Producto> buscarProductos(@RequestParam String nombre) {
        return productoRepository.findByNombreContaining(nombre);
    }

    @PostMapping
    public ResponseEntity<Producto> crearProducto(@RequestBody Producto producto) {
        Producto nuevo = productoRepository.save(producto);
        return new ResponseEntity<>(nuevo, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Producto> actualizarProducto(@PathVariable int id, @RequestBody Producto producto) {
        return productoRepository.findById(id)
                .map(p -> {
                    p.setNombre(producto.getNombre());
                    p.setDescripcion(producto.getDescripcion());
                    p.setStock(producto.getStock());
                    p.setPrecio(producto.getPrecio());
                    p.setCategoria(producto.getCategoria());
                    p.setMarca(producto.getMarca());
                    p.setProveedor(producto.getProveedor());
                    return ResponseEntity.ok(productoRepository.save(p));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @PatchMapping("/{id}/stock")
    public ResponseEntity<Producto> actualizarStock(@PathVariable int id, @RequestParam int nuevoStock) {
        return productoRepository.findById(id)
                .map(p -> {
                    p.setStock(nuevoStock);
                    return ResponseEntity.ok(productoRepository.save(p));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarProducto(@PathVariable int id) {
        return productoRepository.findById(id)
                .map(p -> {
                    productoRepository.delete(p);
                    return ResponseEntity.ok().<Void>build();
                })
                .orElse(ResponseEntity.notFound().build());
    }
}