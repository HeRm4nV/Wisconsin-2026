# Wisconsin Card Sorting Task (WCST) - Protocolo Experimental

## Descripción General

Este experimento implementa una versión adaptada del **Wisconsin Card Sorting Task (WCST)**, una prueba neuropsicológica diseñada para evaluar funciones ejecutivas, flexibilidad cognitiva y capacidad de cambio de set mental.

## Información del Experimento

- **Nombre**: Wisconsin Task
- **Versión**: 0.1
- **Python Version**: 3.11
- **Autor**: [Tu nombre/institución]

## Estructura del Experimento

### Configuración de Bloques

El experimento consta de **4 bloques** con las siguientes características:

| Bloque | Distribución de Mazos | Total de Ensayos |
|--------|----------------------|------------------|
| 1      | 60 + 45              | 105              |
| 2      | 15 + 60 + 30         | 105              |
| 3      | 30 + 60 + 15         | 105              |
| 4      | 45 + 60              | 105              |

**Total del experimento**: 420 ensayos (4 bloques × 105 ensayos)

### Estructura de Series

Cada bloque contiene **15 series** con la siguiente distribución:

- **5 series de 6 ensayos** (30 ensayos)
- **5 series de 7 ensayos** (35 ensayos)
- **5 series de 8 ensayos** (40 ensayos)

**Total por bloque**: 105 ensayos

> **Nota**: El orden de las series se aleatoriza en cada bloque para evitar efectos de orden.

### Tipos de Estímulos

El experimento utiliza tres tipos de estímulos visuales:

1. **Singles (Cartas Individuales)**
   - 24 cartas únicas
   - Ubicación: `media/images/Single/`
   - Cada serie comienza con **2 cartas individuales obligatorias**

2. **Doubles (Cartas Dobles)**
   - 36 cartas únicas
   - Ubicación: `media/images/Double/`
   - Se mezclan con las singles después de las 2 obligatorias

3. **Static (Cartas Estáticas)**
   - Ubicación: `media/images/Static/`
   - [Describir uso específico si aplica]

### Algoritmo de Distribución

El experimento implementa un sistema sofisticado de distribución de cartas:

1. **Proporción Mantenida**: Las cartas singles y doubles mantienen su proporción original (24:36 ≈ 40:60) a través de todos los mazos.

2. **Inicialización de Series**:
   - Cada serie nueva recibe 2 cartas singles obligatorias
   - El resto se completa con una mezcla proporcional de singles y doubles

3. **Reutilización de Cartas**:
   - Las cartas no utilizadas en un mazo se transfieren al siguiente
   - Esto permite una distribución eficiente a través de múltiples mazos por bloque

## Protocolo de Administración

### Inicio del Experimento

1. **Pantalla de Bienvenida**
   ```
   Bienvenido/a, a este experimento!!!
   
   Se te indicará paso a paso que hacer.
   ```

2. El experimento inicia automáticamente en **modo pantalla completa**

### Durante los Bloques

- Se presentan las cartas de acuerdo a la estructura de series definida

### Descansos

Entre bloques se presenta:
```
- TODO
```

### Finalización

```
La tarea ha finalizado.

Muchas gracias por su colaboración!!
```

## Controles del Experimento

| Tecla | Función |
|-------|---------|
| `ESC` | Salir del experimento |
| `SPACE` | Continuar (en pantallas de instrucciones) |
| `ENTER` | Continuar (alternativa) |

## Registro de Datos

### Directorios de Salida

- **`data/`**: Datos experimentales y logs de sesión
- **`debug_data/`**: Archivos de depuración y validación

### Archivos Generados

1. **Archivo ZIP de Debug** (modo debug activo):
   - `debug_blocks_YYYY-MM-DD_HH-MM-SS.zip`
   - Contiene:
     - `debug_blocks_structure.txt`: Estructura global de todos los bloques
     - `debug_block_1.txt` a `debug_block_4.txt`: Detalle de cada bloque

### Metadata de Sesión

Cada sesión genera un timestamp único:
- Formato: `YYYYMMDD_HHMMSS`
- Usado para nombrar archivos y identificar sesiones

## Integración EEG

El experimento incluye soporte para registro EEG mediante:

### Puerto Paralelo (LPT)
```python
init_lpt(address)       # Inicializar puerto paralelo
send_trigger(trigger, address, latency)  # Enviar triggers
```
> **Requisito**: `dlportio.dll` (solo Windows)

### Puerto Serial (COM)
```python
init_com(address="COM3")  # Inicializar puerto serial
send_triggert(trigger)     # Enviar trigger
close_com()                # Cerrar puerto
```

## Requisitos del Sistema

### Software
- Python 3.11
- pygame 2.5.2
- pyserial 3.5

### Hardware
- Resolución mínima: 1280×720
- Se recomienda pantalla completa para mejor experiencia

### Archivos Necesarios

```
Wisconsin/
├── home version.py
├── requirements.txt
├── data/
├── debug_data/
└── media/
    ├── Arial_Rounded_MT_Bold.ttf
    └── images/
        ├── Single/     # 24 imágenes
        ├── Double/     # 36 imágenes
        └── Static/     # Imágenes estáticas
```

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_del_repositorio]
cd Wisconsin
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Verificar estructura de archivos:
```bash
python home version.py
```

## Modo Debug

Para activar el modo debug, modificar en [home version.py](home%20version.py):

```python
debug = True
```

Esto habilitará:
- Mensajes de depuración en consola
- Generación de archivos de validación
- Información detallada de carga de imágenes

## Notas Importantes

1. **Aleatorización**: Las cartas singles y doubles se aleatorizan al inicio de cada sesión
2. **Validación**: El sistema valida automáticamente que cada bloque tenga exactamente 105 ensayos
3. **Proporcionalidad**: Se mantiene la proporción 40:60 (singles:doubles) en todos los mazos
4. **Continuidad**: Las cartas sobrantes de un mazo se reutilizan en el siguiente

## Solución de Problemas

### Error: "Image folder not found"
- Verificar que existan las carpetas `media/images/Single/` y `media/images/Double/`
- Asegurar que contengan imágenes válidas

### Error: "Parallel port could not be opened"
- Verificar instalación de `dlportio.dll` (Windows)
- Comprobar permisos de administrador

### Error: "Serial port could not be opened"
- Verificar que el puerto COM esté disponible
- Comprobar que no esté siendo usado por otra aplicación

## Referencias

Wisconsin Card Sorting Task (WCST) - Prueba neuropsicológica estándar para evaluación de funciones ejecutivas.

## Contacto

Para preguntas o soporte, contactar a: [tu_email@institucion.edu]

---

**Última actualización**: [Fecha]
**Versión del documento**: 1.0