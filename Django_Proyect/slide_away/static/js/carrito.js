document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de carrito con API cargado');
    
    // Recuperar carrito del localStorage o inicializar vacío
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    
    // Función para obtener producto desde la API
    async function obtenerProductoAPI(productoId) {
        try {
            const response = await fetch(`/api/producto/${productoId}/`);
            if (response.ok) {
                return await response.json();
            } else {
                console.error(`Error al obtener producto ${productoId}:`, response.status);
                return null;
            }
        } catch (error) {
            console.error(`Error al obtener producto ${productoId}:`, error);
            return null;
        }
    }
    
    // Función para obtener múltiples productos desde la API
    async function obtenerProductosCarritoAPI(idsProductos) {
        try {
            const response = await fetch('/api/carrito/productos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ids: idsProductos })
            });
            
            if (response.ok) {
                const data = await response.json();
                return data.productos;
            } else {
                console.error('Error al obtener productos del carrito:', response.status);
                return [];
            }
        } catch (error) {
            console.error('Error al obtener productos del carrito:', error);
            return [];
        }
    }
    
    // Función para agregar al carrito
    async function agregarAlCarrito(producto) {
        console.log('Agregando producto al carrito:', producto);
        
        const existe = carrito.find(item => item.id === producto.id);
        
        if (existe) {
            existe.cantidad++;
            console.log(`Producto ${producto.nombre} ya existía. Nueva cantidad: ${existe.cantidad}`);
        } else {
            // Obtener datos completos del producto desde la API
            const productoCompleto = await obtenerProductoAPI(producto.id);
            
            if (productoCompleto) {
                carrito.push({
                    id: productoCompleto.id,
                    nombre: productoCompleto.nombre,
                    descripcion: productoCompleto.descripcion,
                    precio: parseFloat(productoCompleto.precio),
                    stock: productoCompleto.stock,
                    categoria: productoCompleto.categoria,
                    marca: productoCompleto.marca,
                    proveedor: productoCompleto.proveedor,
                    cantidad: 1,
                    modalidadEntrega: 'despacho'
                });
                console.log(`Producto ${productoCompleto.nombre} agregado con datos completos`);
            } else {
                // Fallback con datos básicos si falla la API
                carrito.push({
                    id: producto.id,
                    nombre: producto.nombre,
                    precio: parseFloat(producto.precio),
                    cantidad: 1,
                    modalidadEntrega: 'despacho'
                });
                console.log(`Producto agregado con datos básicos`);
            }
        }
        
        // Guardar en localStorage
        localStorage.setItem('carrito', JSON.stringify(carrito));
        console.log('Carrito guardado en localStorage:', carrito);
        
        // Actualizar contador
        actualizarContadorCarrito();
        
        // Mostrar mensaje de confirmación
        mostrarMensaje(`${producto.nombre} agregado al carrito`);
    }
    
    // Función para actualizar contador del carrito
    function actualizarContadorCarrito() {
        const contador = carrito.reduce((total, item) => total + item.cantidad, 0);
        const carritoBtn = document.getElementById('carritoBtn');
        
        if (carritoBtn) {
            if (contador > 0) {
                carritoBtn.innerHTML = `<i class="fas fa-shopping-cart me-1"></i>Carrito (${contador})`;
                carritoBtn.classList.remove('btn-warning');
                carritoBtn.classList.add('btn-success');
            } else {
                carritoBtn.innerHTML = `<i class="fas fa-shopping-cart me-1"></i>Carrito`;
                carritoBtn.classList.remove('btn-success');
                carritoBtn.classList.add('btn-warning');
            }
        }
        
        console.log(`Contador actualizado: ${contador} productos en el carrito`);
    }
    
    // Función para mostrar mensajes de notificación
    function mostrarMensaje(mensaje) {
        // Remover notificación anterior si existe
        const notificacionAnterior = document.querySelector('.notificacion-carrito');
        if (notificacionAnterior) {
            notificacionAnterior.remove();
        }
        
        // Crear nueva notificación
        const notificacion = document.createElement('div');
        notificacion.className = 'alert alert-success position-fixed notificacion-carrito';
        notificacion.style.cssText = `
            top: 20px; 
            right: 20px; 
            z-index: 9999; 
            max-width: 300px;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
        `;
        notificacion.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>${mensaje}
            <button type="button" class="btn-close ms-2" aria-label="Close"></button>
        `;
        
        document.body.appendChild(notificacion);
        
        // Animar entrada
        setTimeout(() => {
            notificacion.style.opacity = '1';
        }, 100);
        
        // Agregar funcionalidad al botón cerrar
        const btnCerrar = notificacion.querySelector('.btn-close');
        btnCerrar.addEventListener('click', () => {
            notificacion.style.opacity = '0';
            setTimeout(() => {
                if (notificacion.parentNode) {
                    notificacion.remove();
                }
            }, 300);
        });
        
        // Remover automáticamente después de 3 segundos
        setTimeout(() => {
            if (notificacion.parentNode) {
                notificacion.style.opacity = '0';
                setTimeout(() => {
                    if (notificacion.parentNode) {
                        notificacion.remove();
                    }
                }, 300);
            }
        }, 3000);
    }
    
    // Función para mostrar el contenido del carrito
    function mostrarCarrito() {
        if (carrito.length === 0) {
            alert('El carrito está vacío');
            return;
        }
        
        // Redirigir a la página del carrito
        window.location.href = '/carrito/';
    }
    
    // Función para vaciar el carrito
    function vaciarCarrito() {
        carrito = [];
        localStorage.removeItem('carrito');
        actualizarContadorCarrito();
        mostrarMensaje('Carrito vaciado correctamente');
        console.log('Carrito vaciado');
        
        // Recargar página del carrito si estamos en ella
        if (window.location.pathname === '/carrito/') {
            window.location.reload();
        }
    }
    
    // Event listener para botones de agregar al carrito
    document.addEventListener('click', function(e) {
        const botonCarrito = e.target.closest('.agregar-carrito');
        
        if (botonCarrito && !botonCarrito.disabled) {
            e.preventDefault();
            
            const producto = {
                id: botonCarrito.dataset.productoId,
                nombre: botonCarrito.dataset.productoNombre,
                precio: botonCarrito.dataset.productoPrecio
            };
            
            // Validar que los datos estén completos
            if (!producto.id || !producto.nombre || !producto.precio) {
                console.error('Datos del producto incompletos:', producto);
                mostrarMensaje('Error: Datos del producto incompletos');
                return;
            }
            
            agregarAlCarrito(producto);
        }
    });
    
    // Event listener para el botón del carrito
    const carritoBtn = document.getElementById('carritoBtn');
    if (carritoBtn) {
        carritoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            mostrarCarrito();
        });
    }
    
    // Funciones globales para uso externo
    window.obtenerCarrito = function() {
        return carrito;
    };
    
    window.agregarProductoAlCarrito = function(producto) {
        agregarAlCarrito(producto);
    };
    
    window.actualizarContadorCarrito = actualizarContadorCarrito;
    window.obtenerProductosCarritoAPI = obtenerProductosCarritoAPI;
    
    // Actualizar contador al cargar la página
    actualizarContadorCarrito();
    
    console.log('Carrito inicial cargado:', carrito);
});