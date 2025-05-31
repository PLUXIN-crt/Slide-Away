document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de carrito cargado');
    
    // Recuperar carrito del localStorage o inicializar vacío
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    
    // Función para agregar al carrito
    function agregarAlCarrito(producto) {
        console.log('Agregando producto al carrito:', producto);
        
        const existe = carrito.find(item => item.id === producto.id);
        
        if (existe) {
            existe.cantidad++;
            console.log(`Producto ${producto.nombre} ya existía. Nueva cantidad: ${existe.cantidad}`);
        } else {
            carrito.push({
                id: producto.id,
                nombre: producto.nombre,
                precio: parseFloat(producto.precio),
                cantidad: 1
            });
            console.log(`Producto ${producto.nombre} agregado por primera vez`);
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
        
        let contenido = 'CARRITO DE COMPRAS:\n\n';
        let total = 0;
        
        carrito.forEach(item => {
            const subtotal = item.precio * item.cantidad;
            contenido += `${item.nombre}\n`;
            contenido += `Precio: $${item.precio.toFixed(2)}\n`;
            contenido += `Cantidad: ${item.cantidad}\n`;
            contenido += `Subtotal: $${subtotal.toFixed(2)}\n\n`;
            total += subtotal;
        });
        
        contenido += `TOTAL: $${total.toFixed(2)}`;
        
        // Mostrar contenido del carrito
        const mostrarDetalle = confirm(contenido + '\n\n¿Deseas vaciar el carrito?');
        
        if (mostrarDetalle) {
            vaciarCarrito();
        }
    }
    
    // Función para vaciar el carrito
    function vaciarCarrito() {
        carrito = [];
        localStorage.removeItem('carrito');
        actualizarContadorCarrito();
        mostrarMensaje('Carrito vaciado correctamente');
        console.log('Carrito vaciado');
    }
    
    // Event listener para botones de agregar al carrito
    document.addEventListener('click', function(e) {
        // Verificar si el click es en un botón de agregar al carrito o su icono
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
    
    // Función para obtener datos del carrito (para uso externo)
    window.obtenerCarrito = function() {
        return carrito;
    };
    
    // Función para agregar producto desde código externo
    window.agregarProductoAlCarrito = function(producto) {
        agregarAlCarrito(producto);
    };
    
    // Actualizar contador al cargar la página
    actualizarContadorCarrito();
    
    console.log('Carrito inicial cargado:', carrito);
});