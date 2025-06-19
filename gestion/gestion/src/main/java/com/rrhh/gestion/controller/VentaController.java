package com.rrhh.gestion.controller;

import com.rrhh.gestion.dto.VentaDTO;
import com.rrhh.gestion.entity.*;
import com.rrhh.gestion.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/ventas")
@CrossOrigin(origins = "*")
public class VentaController {

    @Autowired
    private VentaRepository ventaRepository;
    
    @Autowired
    private ClienteRepository clienteRepository;
    
    @Autowired
    private TipoPagoRepository tipoPagoRepository;
    
    @Autowired
    private SucursalRepository sucursalRepository;

    // Obtener todas las ventas
    @GetMapping
    public ResponseEntity<List<VentaDTO>> getAllVentas() {
        List<Venta> ventas = ventaRepository.findAll();
        List<VentaDTO> ventasDTO = ventas.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(ventasDTO);
    }

    // Buscar venta por número de documento
    @GetMapping("/{numeroDocumento}")
    public ResponseEntity<VentaDTO> getVentaById(@PathVariable Integer numeroDocumento) {
        Optional<Venta> venta = ventaRepository.findById(numeroDocumento);
        if (venta.isPresent()) {
            return ResponseEntity.ok(convertToDTO(venta.get()));
        }
        return ResponseEntity.notFound().build();
    }

    // Buscar ventas por RUT de cliente
    @GetMapping("/cliente/{rutCliente}")
    public ResponseEntity<List<VentaDTO>> getVentasByCliente(@PathVariable String rutCliente) {
        List<Venta> ventas = ventaRepository.findByClienteRut(rutCliente);
        List<VentaDTO> ventasDTO = ventas.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(ventasDTO);
    }

    // Buscar ventas por rango de fechas
    @GetMapping("/fecha")
    public ResponseEntity<List<VentaDTO>> getVentasByFecha(
            @RequestParam LocalDate fechaInicio,
            @RequestParam LocalDate fechaFin) {
        List<Venta> ventas = ventaRepository.findByFechaVentaBetween(fechaInicio, fechaFin);
        List<VentaDTO> ventasDTO = ventas.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(ventasDTO);
    }

    // Crear nueva venta
    @PostMapping
    public ResponseEntity<VentaDTO> createVenta(@RequestBody VentaDTO ventaDTO) {
        try {
            Venta venta = convertToEntity(ventaDTO);
            Venta ventaGuardada = ventaRepository.save(venta);
            return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(ventaGuardada));
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // Actualizar venta existente
    @PutMapping("/{numeroDocumento}")
    public ResponseEntity<VentaDTO> updateVenta(@PathVariable Integer numeroDocumento, @RequestBody VentaDTO ventaDTO) {
        Optional<Venta> ventaExistente = ventaRepository.findById(numeroDocumento);
        if (ventaExistente.isPresent()) {
            try {
                Venta venta = ventaExistente.get();
                venta.setTipoDocumento(ventaDTO.getTipoDocumento());
                venta.setFechaVenta(ventaDTO.getFechaVenta());
                venta.setTotalVenta(ventaDTO.getTotalVenta());
                venta.setNombreCliente(ventaDTO.getNombreCliente());
                venta.setApellidoCliente(ventaDTO.getApellidoCliente());
                
                // Actualizar relaciones si es necesario
                if (ventaDTO.getIdTipoPago() != null) {
                    TipoPago tipoPago = tipoPagoRepository.findById(ventaDTO.getIdTipoPago())
                            .orElseThrow(() -> new RuntimeException("Tipo de pago no encontrado"));
                    venta.setTipoPago(tipoPago);
                }
                
                if (ventaDTO.getRutCliente() != null) {
                    Cliente cliente = clienteRepository.findById(ventaDTO.getRutCliente())
                            .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));
                    venta.setCliente(cliente);
                }
                
                if (ventaDTO.getIdSucursal() != null) {
                    Sucursal sucursal = sucursalRepository.findById(ventaDTO.getIdSucursal())
                            .orElseThrow(() -> new RuntimeException("Sucursal no encontrada"));
                    venta.setSucursal(sucursal);
                }
                
                Venta ventaActualizada = ventaRepository.save(venta);
                return ResponseEntity.ok(convertToDTO(ventaActualizada));
            } catch (Exception e) {
                return ResponseEntity.badRequest().build();
            }
        }
        return ResponseEntity.notFound().build();
    }

    // Eliminar venta
    @DeleteMapping("/{numeroDocumento}")
    public ResponseEntity<Void> deleteVenta(@PathVariable Integer numeroDocumento) {
        if (ventaRepository.existsById(numeroDocumento)) {
            ventaRepository.deleteById(numeroDocumento);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    // Métodos de conversión
    private VentaDTO convertToDTO(Venta venta) {
        VentaDTO dto = new VentaDTO();
        dto.setNumeroDocumento(venta.getNumeroDocumento());
        dto.setTipoDocumento(venta.getTipoDocumento());
        dto.setFechaVenta(venta.getFechaVenta());
        dto.setTotalVenta(venta.getTotalVenta());
        dto.setNombreCliente(venta.getNombreCliente());
        dto.setApellidoCliente(venta.getApellidoCliente());
        
        if (venta.getTipoPago() != null) {
            dto.setIdTipoPago(venta.getTipoPago().getIdTipoPago());
            dto.setNombreTipoPago(venta.getTipoPago().getNombre());
        }
        
        if (venta.getCliente() != null) {
            dto.setRutCliente(venta.getCliente().getRut());
        }
        
        if (venta.getSucursal() != null) {
            dto.setIdSucursal(venta.getSucursal().getIdSucursal());
            dto.setNombreSucursal(venta.getSucursal().getNombreSucursal());
        }
        
        return dto;
    }

    private Venta convertToEntity(VentaDTO dto) {
        Venta venta = new Venta();
        venta.setNumeroDocumento(dto.getNumeroDocumento());
        venta.setTipoDocumento(dto.getTipoDocumento());
        venta.setFechaVenta(dto.getFechaVenta());
        venta.setTotalVenta(dto.getTotalVenta());
        venta.setNombreCliente(dto.getNombreCliente());
        venta.setApellidoCliente(dto.getApellidoCliente());
        
        if (dto.getIdTipoPago() != null) {
            TipoPago tipoPago = tipoPagoRepository.findById(dto.getIdTipoPago())
                    .orElseThrow(() -> new RuntimeException("Tipo de pago no encontrado"));
            venta.setTipoPago(tipoPago);
        }
        
        if (dto.getRutCliente() != null) {
            Cliente cliente = clienteRepository.findById(dto.getRutCliente())
                    .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));
            venta.setCliente(cliente);
        }
        
        if (dto.getIdSucursal() != null) {
            Sucursal sucursal = sucursalRepository.findById(dto.getIdSucursal())
                    .orElseThrow(() -> new RuntimeException("Sucursal no encontrada"));
            venta.setSucursal(sucursal);
        }
        
        return venta;
    }
}
