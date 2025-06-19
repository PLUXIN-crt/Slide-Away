package com.rrhh.gestion.controller;

import com.rrhh.gestion.dto.ClienteDTO;
import com.rrhh.gestion.entity.Cliente;
import com.rrhh.gestion.entity.Comuna;
import com.rrhh.gestion.repository.ClienteRepository;
import com.rrhh.gestion.repository.ComunaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/clientes")
@CrossOrigin(origins = "*")
public class ClienteController {

    @Autowired
    private ClienteRepository clienteRepository;
    
    @Autowired
    private ComunaRepository comunaRepository;

    // Obtener todos los clientes
    @GetMapping
    public ResponseEntity<List<ClienteDTO>> getAllClientes() {
        List<Cliente> clientes = clienteRepository.findAll();
        List<ClienteDTO> clientesDTO = clientes.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(clientesDTO);
    }

    // Buscar cliente por RUT
    @GetMapping("/{rut}")
    public ResponseEntity<ClienteDTO> getClienteByRut(@PathVariable String rut) {
        Optional<Cliente> cliente = clienteRepository.findById(rut);
        if (cliente.isPresent()) {
            return ResponseEntity.ok(convertToDTO(cliente.get()));
        }
        return ResponseEntity.notFound().build();
    }

    // Buscar clientes por nombre o apellidos
    @GetMapping("/buscar")
    public ResponseEntity<List<ClienteDTO>> buscarClientes(@RequestParam String termino) {
        List<Cliente> clientes = clienteRepository.findByNombreOrApellidosContainingIgnoreCase(termino, termino);
        List<ClienteDTO> clientesDTO = clientes.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(clientesDTO);
    }

    // Crear nuevo cliente
    @PostMapping
    public ResponseEntity<ClienteDTO> createCliente(@RequestBody ClienteDTO clienteDTO) {
        try {
            Cliente cliente = convertToEntity(clienteDTO);
            Cliente clienteGuardado = clienteRepository.save(cliente);
            return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(clienteGuardado));
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // Actualizar cliente existente
    @PutMapping("/{rut}")
    public ResponseEntity<ClienteDTO> updateCliente(@PathVariable String rut, @RequestBody ClienteDTO clienteDTO) {
        Optional<Cliente> clienteExistente = clienteRepository.findById(rut);
        if (clienteExistente.isPresent()) {
            try {
                Cliente cliente = clienteExistente.get();
                cliente.setNombre(clienteDTO.getNombre());
                cliente.setApellidos(clienteDTO.getApellidos());
                cliente.setTelefono(clienteDTO.getTelefono());
                cliente.setCorreo(clienteDTO.getCorreo());
                
                if (clienteDTO.getIdComuna() != null) {
                    Comuna comuna = comunaRepository.findById(clienteDTO.getIdComuna())
                            .orElseThrow(() -> new RuntimeException("Comuna no encontrada"));
                    cliente.setComuna(comuna);
                }
                
                Cliente clienteActualizado = clienteRepository.save(cliente);
                return ResponseEntity.ok(convertToDTO(clienteActualizado));
            } catch (Exception e) {
                return ResponseEntity.badRequest().build();
            }
        }
        return ResponseEntity.notFound().build();
    }

    // Eliminar cliente
    @DeleteMapping("/{rut}")
    public ResponseEntity<Void> deleteCliente(@PathVariable String rut) {
        if (clienteRepository.existsById(rut)) {
            clienteRepository.deleteById(rut);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    // Métodos de conversión
    private ClienteDTO convertToDTO(Cliente cliente) {
        ClienteDTO dto = new ClienteDTO();
        dto.setRut(cliente.getRut());
        dto.setNombre(cliente.getNombre());
        dto.setApellidos(cliente.getApellidos());
        dto.setTelefono(cliente.getTelefono());
        dto.setCorreo(cliente.getCorreo());
        
        if (cliente.getComuna() != null) {
            dto.setIdComuna(cliente.getComuna().getId());
            dto.setNombreComuna(cliente.getComuna().getNombre());
        }
        
        return dto;
    }

    private Cliente convertToEntity(ClienteDTO dto) {
        Cliente cliente = new Cliente();
        cliente.setRut(dto.getRut());
        cliente.setNombre(dto.getNombre());
        cliente.setApellidos(dto.getApellidos());
        cliente.setTelefono(dto.getTelefono());
        cliente.setCorreo(dto.getCorreo());
        
        if (dto.getIdComuna() != null) {
            Comuna comuna = comunaRepository.findById(dto.getIdComuna())
                    .orElseThrow(() -> new RuntimeException("Comuna no encontrada"));
            cliente.setComuna(comuna);
        }
        
        return cliente;
    }
}
