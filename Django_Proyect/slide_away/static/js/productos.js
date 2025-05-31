document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de imágenes de productos cargado');
    
    // Buscar imágenes tanto del menú como del catálogo
    const images = document.querySelectorAll('[id^="img-producto-"], [id^="img-catalogo-"]');
    const extensiones = ['jpg', 'jpeg', 'png', 'webp', 'gif'];
    
    images.forEach(function(img) {
        const nombreProducto = img.getAttribute('data-nombre-producto');
        
        if (!nombreProducto) {
            console.warn('Imagen sin atributo data-nombre-producto:', img);
            return;
        }
        
        console.log('Procesando producto:', nombreProducto);
        
        // Limpiar el nombre del producto (remover espacios, caracteres especiales)
        const nombreLimpio = nombreProducto
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '') // remover acentos
            .replace(/[^a-z0-9]/g, '-') // reemplazar caracteres especiales con guiones
            .replace(/-+/g, '-') // remover guiones múltiples
            .replace(/^-|-$/g, ''); // remover guiones al inicio y final
        
        console.log('Nombre limpio:', nombreLimpio);
        
        let imagenEncontrada = false;
        let intentoActual = 0;
        
        function probarSiguienteExtension() {
            if (intentoActual < extensiones.length && !imagenEncontrada) {
                const rutaImagen = `/static/images/productos/${nombreLimpio}.${extensiones[intentoActual]}`;
                console.log('Probando ruta:', rutaImagen);
                
                // Crear una imagen temporal para verificar si existe
                const imgTemp = new Image();
                imgTemp.onload = function() {
                    // La imagen existe, asignarla al elemento
                    console.log('Imagen encontrada:', rutaImagen);
                    img.src = rutaImagen;
                    imagenEncontrada = true;
                };
                imgTemp.onerror = function() {
                    // Esta extensión no funciona, probar la siguiente
                    console.log('Imagen no encontrada:', rutaImagen);
                    intentoActual++;
                    probarSiguienteExtension();
                };
                imgTemp.src = rutaImagen;
            } else if (!imagenEncontrada) {
                // No se encontró ninguna imagen, usar la imagen por defecto
                const imagenPorDefecto = '/static/images/productos/imagen_referencia.jpeg';
                console.log('Usando imagen por defecto:', imagenPorDefecto);
                img.src = imagenPorDefecto;
            }
        }
        
        // Iniciar la búsqueda
        probarSiguienteExtension();
    });
});