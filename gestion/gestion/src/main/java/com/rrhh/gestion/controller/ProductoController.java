package com.rrhh.gestion.controller;

import com.rrhh.gestion.dto.ProductoDTO;
import com.rrhh.gestion.entity.*;
import com.rrhh.gestion.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/productos")
@CrossOrigin(origins = "*")
public class ProductoController {

    @Autowired
    private ProductoRepository productoRepository;
    
    @Autowired
    private CategoriaRepository categoriaRepository;
    
    @Autowired
    private MarcaRepository marcaRepository;
    
    @Autowired
    private ProveedorRepository proveedorRepository;

    // Obtener todos los productos
    @GetMapping
    public ResponseEntity<List<ProductoDTO>> getAllProductos() {
        List<Producto> productos = productoRepository.findAll();
        List<ProductoDTO> productosDTO = productos.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(productosDTO);
    }

    // Buscar producto por ID
    @GetMapping("/{id}")
    public ResponseEntity<ProductoDTO> getProductoById(@PathVariable Integer id) {
        Optional<Producto> producto = productoRepository.findById(id);
        if (producto.isPresent()) {
            return ResponseEntity.ok(convertToDTO(producto.get()));
        }
        return ResponseEntity.notFound().build();
    }

    // Buscar productos por nombre
    @GetMapping("/buscar")
    public ResponseEntity<List<ProductoDTO>> buscarProductosPorNombre(@RequestParam String nombre) {
        List<Producto> productos = productoRepository.findByNombreContainingIgnoreCase(nombre);
        List<ProductoDTO> productosDTO = productos.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(productosDTO);
    }

    // Crear nuevo producto
    @PostMapping
    public ResponseEntity<ProductoDTO> createProducto(@RequestBody ProductoDTO productoDTO) {
        try {
            Producto producto = convertToEntity(productoDTO);
            Producto productoGuardado = productoRepository.save(producto);
            return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(productoGuardado));
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/dto")
    public ResponseEntity<List<ProductoDTO>> getAllProductosDTO() {
        List<Producto> productos = productoRepository.findAll();
        List<ProductoDTO> productosDTO = productos.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(productosDTO);
    }

    // Actualizar producto existente
    @PutMapping("/{id}")
    public ResponseEntity<ProductoDTO> updateProducto(@PathVariable Integer id, @RequestBody ProductoDTO productoDTO) {
        Optional<Producto> productoExistente = productoRepository.findById(id);
        if (productoExistente.isPresent()) {
            try {
                Producto producto = productoExistente.get();
                producto.setNombre(productoDTO.getNombre());
                producto.setDescripcion(productoDTO.getDescripcion());
                producto.setStock(productoDTO.getStock());
                producto.setPrecio(productoDTO.getPrecio());
                
                // Actualizar relaciones si es necesario
                if (productoDTO.getIdCategoria() != null) {
                    Categoria categoria = categoriaRepository.findById(productoDTO.getIdCategoria())
                            .orElseThrow(() -> new RuntimeException("Categoría no encontrada"));
                    producto.setCategoria(categoria);
                }
                
                if (productoDTO.getIdMarca() != null) {
                    Marca marca = marcaRepository.findById(productoDTO.getIdMarca())
                            .orElseThrow(() -> new RuntimeException("Marca no encontrada"));
                    producto.setMarca(marca);
                }
                
                if (productoDTO.getIdProveedor() != null) {
                    Proveedor proveedor = proveedorRepository.findById(productoDTO.getIdProveedor())
                            .orElseThrow(() -> new RuntimeException("Proveedor no encontrado"));
                    producto.setProveedor(proveedor);
                }
                
                Producto productoActualizado = productoRepository.save(producto);
                return ResponseEntity.ok(convertToDTO(productoActualizado));
            } catch (Exception e) {
                return ResponseEntity.badRequest().build();
            }
        }
        return ResponseEntity.notFound().build();
    }

    // Eliminar producto
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProducto(@PathVariable Integer id) {
        if (productoRepository.existsById(id)) {
            productoRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    // Métodos de conversión
    private ProductoDTO convertToDTO(Producto producto) {
        ProductoDTO dto = new ProductoDTO();
        dto.setId(producto.getId());
        dto.setNombre(producto.getNombre());
        dto.setDescripcion(producto.getDescripcion());
        dto.setStock(producto.getStock());
        dto.setPrecio(producto.getPrecio());
        
        if (producto.getCategoria() != null) {
            dto.setIdCategoria(producto.getCategoria().getId());
            dto.setNombreCategoria(producto.getCategoria().getNombre());
        }
        
        if (producto.getMarca() != null) {
            dto.setIdMarca(producto.getMarca().getId());
            dto.setNombreMarca(producto.getMarca().getNombre());
        }
        
        if (producto.getProveedor() != null) {
            dto.setIdProveedor(producto.getProveedor().getId());
            dto.setNombreProveedor(producto.getProveedor().getNombre());
        }
        
        return dto;
    }

    private Producto convertToEntity(ProductoDTO dto) {
        Producto producto = new Producto();
        producto.setNombre(dto.getNombre());
        producto.setDescripcion(dto.getDescripcion());
        producto.setStock(dto.getStock());
        producto.setPrecio(dto.getPrecio());
        
        if (dto.getIdCategoria() != null) {
            Categoria categoria = categoriaRepository.findById(dto.getIdCategoria())
                    .orElseThrow(() -> new RuntimeException("Categoría no encontrada"));
            producto.setCategoria(categoria);
        }
        
        if (dto.getIdMarca() != null) {
            Marca marca = marcaRepository.findById(dto.getIdMarca())
                    .orElseThrow(() -> new RuntimeException("Marca no encontrada"));
            producto.setMarca(marca);
        }
        
        if (dto.getIdProveedor() != null) {
            Proveedor proveedor = proveedorRepository.findById(dto.getIdProveedor())
                    .orElseThrow(() -> new RuntimeException("Proveedor no encontrado"));
            producto.setProveedor(proveedor);
        }
        
        return producto;
    }
}
