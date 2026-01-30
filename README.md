# Wisconsin Card Sorting Task (WCST) - Protocolo Experimental

## Descripción General

Este experimento implementa una versión adaptada del **Wisconsin Card Sorting Task (WCST)**, una prueba neuropsicológica diseñada para evaluar funciones ejecutivas, flexibilidad cognitiva y capacidad de cambio de set mental.

## Información del Experimento

- **Nombre**: Wisconsin Task
- **Versión**: 0.2
- **Python Version**: 3.11
- **Autor**: Herman Valencia

---

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

---

## Reglas de Clasificación

El experimento utiliza **3 reglas de clasificación** que se presentan en orden balanceado:

### Tipos de Reglas

1. **Número** (`"number"`): Emparejar según la cantidad de elementos
2. **Color** (`"color"`): Emparejar según el color de los elementos
3. **Figura** (`"figure"`): Emparejar según la forma de los elementos

### Distribución de Reglas

- Cada bloque tiene **15 series** (5 iteraciones de las 3 reglas)
- En cada iteración, las 3 reglas se aleatorizan
- **Restricción importante**: La primera regla de una nueva iteración nunca puede ser igual a la última regla de la iteración anterior
- Esto asegura cambios de regla claros entre series consecutivas

### Cartas de Referencia

El experimento utiliza **4 cartas de referencia estáticas** ubicadas en la parte superior de la pantalla:

| Posición | Tecla | Descripción | Archivo |
|----------|-------|-------------|---------|
| 1 (Izquierda) | **C** | Triángulo rojo | `Static/` |
| 2 | **V** | Dos estrellas verdes | `Static/` |
| 3 | **B** | Tres cruces amarillas | `Static/` |
| 4 (Derecha) | **N** | Cuatro círculos azules | `Static/` |

---

## Tipos de Estímulos

El experimento utiliza tres categorías de estímulos visuales:

### 1. Singles (Cartas Individuales)
- **Cantidad**: 24 cartas únicas
- **Ubicación**: `media/images/Single/`
- **Uso**: Cada serie comienza con **2 cartas singles obligatorias**

### 2. Doubles (Cartas Dobles)
- **Cantidad**: 36 cartas únicas
- **Ubicación**: `media/images/Double/`
- **Uso**: Se mezclan con las singles después de las 2 obligatorias

### 3. Static (Cartas de Referencia)
- **Cantidad**: 4 cartas fijas
- **Ubicación**: `media/images/Static/`
- **Uso**: Siempre visibles en la parte superior de la pantalla

### Nomenclatura de Archivos

Las imágenes deben seguir el formato:
```
[número]_[figura]_[color].png
```

**Ejemplo**: `1_triangle_red.png`

---

## Algoritmo de Distribución de Cartas

El experimento implementa un sistema sofisticado de distribución basado en **DeckCursor**:

### 1. Proporción Mantenida
- Las cartas singles y doubles mantienen su proporción original (24:36 ≈ 40:60)
- Esta proporción se respeta en todos los mazos del experimento

### 2. Sistema de Mazos Múltiples
- Cada bloque puede tener múltiples mazos (según `deck_sizes_per_block`)
- Los mazos se consumen secuencialmente a través de las series
- **Planificación automática**: El sistema calcula qué series consume cada mazo

### 3. Inicialización de Series

Para cada serie:

1. **Reserva proporcional**: Se calculan cuántas singles y doubles se necesitan del mazo actual
2. **Singles obligatorias**: Se añaden 2 cartas singles al inicio de cada serie nueva
3. **Mezcla balanceada**: Las singles y doubles restantes se mezclan aleatoriamente
4. **Relleno de series**: Se completa cada serie hasta su tamaño objetivo

### 4. Reutilización de Cartas

- Las cartas **no utilizadas** en un mazo se transfieren automáticamente al siguiente
- Esto permite distribución eficiente a través de múltiples mazos por bloque
- Se mantiene la proporción 40:60 en cada transferencia

### 5. Validación Automática

El sistema valida que:
- Cada bloque tenga exactamente 105 ensayos
- No haya series vacías
- Todas las cartas obligatorias estén presentes

---

## Protocolo de Administración

### Instrucciones Iniciales

```
¡Bienvenida/o! Este experimento consta de cuatro bloques con
descansos de 2 a 3 minutos entre ellos. Durante las pausas aparecerá el
mensaje "Fin del bloque X", y deberás esperar la indicación para continuar.

En cada ensayo, deberás emparejar la carta central con una de las
cuatro cartas de referencia ubicadas en la parte superior. La selección
se basa en una regla que puede ser color, forma o número, la cual no
se indicará y puede cambiar sin previo aviso.

Tras cada respuesta, recibirás retroalimentación de "Correcto" o
"Incorrecto", que deberás usar para inferir la regla vigente.

Para responder, presiona la tecla correspondiente según la posición
de la carta de referencia de izquierda a derecha:
C (triángulo rojo), V (dos estrellas verdes),
B (tres cruces amarillas) y N (cuatro círculos azules).

Responde lo más rápido posible.
```

### Secuencia de Cada Ensayo

1. **Fijación** (600 ms inicialmente, luego 1500-2000 ms aleatorio)
   - Se presenta una cruz de fijación (`+`) en el centro de la pantalla

2. **Presentación del Estímulo**
   - Se muestra la carta objetivo en el centro inferior
   - Las 4 cartas de referencia permanecen visibles arriba
   - El participante responde usando las teclas **C**, **V**, **B**, o **N**

3. **Retroalimentación** (1500 ms)
   - **Correcto**: ✓ verde en el centro de la pantalla
   - **Incorrecto**: ✗ roja en el centro de la pantalla

### Descansos Entre Bloques

```
Fin del bloque [N].

Tómate de 2 a 3 minutos para descansar.

Cuando estés lista/o para continuar presiona la barra espaciadora.
```

### Finalización

```
La tarea ha finalizado.

Muchas gracias por su colaboración!!
```

---

## Controles del Experimento

| Tecla | Función |
|-------|---------|
| `ESC` | Salir del experimento |
| `SPACE` | Continuar (en pantallas de instrucciones) |
| `ENTER` | Continuar (alternativa) |
| `C` | Seleccionar carta 1 (triángulo rojo) |
| `V` | Seleccionar carta 2 (dos estrellas verdes) |
| `B` | Seleccionar carta 3 (tres cruces amarillas) |
| `N` | Seleccionar carta 4 (cuatro círculos azules) |
| `P` | Saltar bloque (solo en modo debug) |

---

## Sistema de Triggers EEG

> ⚠️ **NOTA**: El sistema de triggers está en proceso de actualización y ampliación en la última versión del código.

### Triggers Implementados

| Evento | Código | Descripción |
|--------|--------|-------------|
| Inicio del experimento | `254` | Marca el comienzo de la sesión |
| Fin del experimento | `255` | Marca el final de la sesión |

### Integración Hardware

#### Puerto Paralelo (LPT)
```python
init_lpt(address=0xD100)
send_trigger(trigger, address, latency=5)
```
- **Requisito**: `dlportio.dll` (solo Windows)
- **Permisos**: Requiere privilegios de administrador
- **Uso**: Para sistemas EEG tradicionales

#### Puerto Serial (COM)
```python
init_com(address="COM3")
send_triggert(trigger)
close_com()
```
- **Baudrate**: 115200
- **Formato**: 1 byte por trigger
- **Uso**: Para sistemas EEG modernos con interfaz serial

### Latencia de Triggers

- **Latencia configurada**: 5 ms
- **Función**: `sleepy_trigger(trigger, latency=100)`
- El sistema espera la latencia especificada antes de resetear el puerto

---

## Registro de Datos

### Estructura de Directorios

```
Wisconsin/
├── data/               # Datos experimentales y logs
├── debug_data/         # Archivos de depuración (ZIP)
└── media/
    ├── Arial_Rounded_MT_Bold.ttf
    └── images/
        ├── Single/     # 24 cartas individuales
        ├── Double/     # 36 cartas dobles
        └── Static/     # 4 cartas de referencia
```

### Archivos Generados

#### 1. Archivo ZIP de Depuración

**Nombre**: `debug_blocks_YYYY-MM-DD_HH-MM-SS.zip`

**Ubicación**: `debug_data/`

**Contenido**:

- `debug_blocks_structure.txt`: Estructura global de los 4 bloques
  - Tamaños de series por bloque
  - Distribución de mazos
  - Plan de consumo de mazos por series

- `debug_block_1.txt` a `debug_block_4.txt`: Detalles de cada bloque
  - Lista completa de cartas por serie
  - Orden exacto de presentación
  - Validación de tamaños

**Ejemplo de `debug_blocks_structure.txt`**:
```
Global Blocks Structure

Estructura del bloque 1

Serie 1: Tamaño 7
Serie 2: Tamaño 6
...
Serie 15: Tamaño 8

Distribución de mazos:
  Mazo 1 (tamaño 60): series 1 a 9
    Serie 1: usa 7 slots
    Serie 2: usa 6 slots
    ...
  Mazo 2 (tamaño 45): series 9 a 15
    ...
```

#### 2. Archivo de Datos Experimentales (Planificado)

**Formato CSV** con las siguientes columnas:

| Campo | Descripción |
|-------|-------------|
| `Sujeto` | ID del participante |
| `IdImagen` | Nombre del archivo de la carta |
| `Bloque` | Número de bloque (1-4) |
| `Serie` | Número de serie dentro del bloque |
| `TipoRegla` | Regla activa (number/color/figure) |
| `TReaccion` | Tiempo de reacción en ms |
| `TipoImagen` | Single o Double |
| `Respuesta` | Tecla presionada (0=C, 1=V, 2=B, 3=N) |
| `Acierto` | 1 si correcto, 0 si incorrecto |

### Metadata de Sesión

- **Timestamp**: `YYYYMMDD_HHMMSS`
- **Formato**: Utilizado para nombrar archivos y ZIP
- **Función**: Identificación única de cada sesión experimental

---

## Requisitos del Sistema

### Software

```
Python 3.11
pygame 2.5.2
pyserial 3.5
```

### Hardware

- **Resolución mínima**: 1280×720 (se recomienda 1920×1080)
- **Modo de pantalla**: Pantalla completa automática
- **Dispositivos**: Teclado obligatorio

### Archivos de Recursos

#### Fuente
- `media/Arial_Rounded_MT_Bold.ttf`

#### Imágenes

**Singles** (24 archivos requeridos):
```
media/images/Single/
├── [imagen1].png
├── [imagen2].png
...
└── [imagen24].png
```

**Doubles** (36 archivos requeridos):
```
media/images/Double/
├── [imagen1].png
├── [imagen2].png
...
└── [imagen36].png
```

**Static** (4 archivos requeridos):
```
media/images/Static/
├── 1_triangle_red.png
├── 2_star_green.png
├── 3_cross_yellow.png
└── 4_circle_blue.png
```

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone [URL_del_repositorio]
cd Wisconsin
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`**:
```txt
pygame==2.5.2
pyserial==3.5
```

### 3. Verificar Estructura de Archivos

```bash
# Verificar que existan las carpetas de imágenes
ls media/images/Single/
ls media/images/Double/
ls media/images/Static/

# Verificar cantidad de archivos
# Singles: 24 archivos
# Doubles: 36 archivos
# Static: 4 archivos
```

### 4. Ejecutar el Experimento

```bash
python "home version.py"
```

---

## Modo Debug

### Activación

Modificar en [`home version.py`](home%20version.py):

```python
debug = True
```

### Funcionalidades Habilitadas

1. **Mensajes en Consola**
   - Información de carga de imágenes
   - Progreso de generación de bloques
   - Detalles de cada ensayo

2. **Archivos de Validación**
   - Generación automática de ZIP en `debug_data/`
   - Estructura completa de bloques
   - Listado de todas las cartas por serie

3. **Controles Adicionales**
   - `P`: Saltar bloque actual
   - `ESC`: Salir en cualquier momento

4. **Información de Respuestas**
   ```python
   print(serie_count, image_count)  # Posición actual
   print(series_type)                # Regla activa
   print(correct_answer)             # Respuesta correcta
   ```

---

## Validación y Calidad de Datos

### Validaciones Automáticas

1. **Cantidad de Ensayos**
   - Cada bloque debe tener exactamente 105 ensayos
   - Error si la suma de mazos ≠ 105

2. **Proporción Singles/Doubles**
   - Se mantiene 40:60 en todos los mazos
   - Validación en cada transferencia entre mazos

3. **Series Completas**
   - Todas las series deben alcanzar su tamaño objetivo
   - No se permiten series incompletas

4. **Singles Obligatorias**
   - Cada serie comienza con 2 singles
   - Error si no hay suficientes singles disponibles

### Verificación Manual

Usar los archivos de debug para verificar:

```bash
# Extraer y revisar el ZIP más reciente
cd debug_data
unzip debug_blocks_[fecha].zip -d temp/
cat temp/debug_blocks_structure.txt
```

---

## Solución de Problemas

### Error: "Image folder not found"

**Causa**: Falta una o más carpetas de imágenes

**Solución**:
```bash
mkdir -p media/images/Single
mkdir -p media/images/Double
mkdir -p media/images/Static
```

### Error: "Invalid deck sizes in block X"

**Causa**: La suma de mazos en un bloque no es 105

**Solución**: Verificar `deck_sizes_per_block` en el código:
```python
deck_sizes_per_block = [
    [60, 45],      # Debe sumar 105
    [15, 60, 30],  # Debe sumar 105
    [30, 60, 15],  # Debe sumar 105
    [45, 60]       # Debe sumar 105
]
```

### Error: "Not enough Singles for mandatory 2 per series"

**Causa**: Proporción incorrecta entre singles y doubles

**Solución**: Verificar que haya al menos:
- **Singles**: 24 imágenes (mínimo: 30 para 15 series × 2)
- **Doubles**: 36 imágenes

### Error: "Parallel port could not be opened"

**Causa**: Falta `dlportio.dll` o permisos insuficientes

**Solución**:
1. Descargar `dlportio.dll` de: [enlace oficial]
2. Copiar a `C:\Windows\System32\` (64-bit) o `C:\Windows\SysWOW64\` (32-bit)
3. Ejecutar como Administrador

### Error: "Serial port could not be opened"

**Causa**: Puerto COM no disponible o en uso

**Solución**:
```python
# Verificar puertos disponibles
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)

# Cambiar puerto en el código
init_com(address="COM4")  # Usar puerto correcto
```

---

## Notas Importantes

### 1. Aleatorización
- Las cartas singles y doubles se aleatorizan **una vez** al inicio de la sesión
- Las reglas de clasificación se aleatorizan por iteración (cada 3 series)
- Los tamaños de series se aleatorizan por bloque

### 2. Continuidad de Mazos
- Las cartas sobrantes de un mazo se **reutilizan automáticamente** en el siguiente
- Esto es transparente para el participante
- Mantiene la proporción 40:60 en todo momento

### 3. Reglas de Clasificación
- **No se repite** la misma regla entre el final de una iteración y el inicio de la siguiente
- Esto garantiza cambios de set mental claros
- El participante debe inferir la regla activa mediante retroalimentación

### 4. Tiempo de Respuesta
- **No hay límite de tiempo** para responder
- Se registra el tiempo de reacción desde la presentación del estímulo
- Se recomienda responder lo más rápido posible

### 5. Archivos Debug
- Los archivos ZIP se generan **automáticamente** en cada sesión si `debug=True`
- **No se sobreescriben**: cada sesión tiene su propio timestamp
- Útiles para validar la estructura del experimento antes de recopilar datos

---

## Cambios Recientes (Última Versión)

### ✅ Implementado

1. **Sistema DeckCursor mejorado**
   - Gestión proporcional de singles y doubles
   - Reutilización eficiente entre mazos

2. **Generación de reglas de clasificación**
   - Función `generate_series_types_for_block()`
   - Balanceo automático de 15 series (5 iteraciones × 3 reglas)
   - Validación de no repetición entre iteraciones

3. **Retroalimentación visual mejorada**
   - ✓ verde para respuestas correctas
   - ✗ roja para respuestas incorrectas
   - Funciones `draw_check()` y `draw_cross()`

4. **Validación de respuestas**
   - Comparación dinámica según regla activa
   - Extracción de atributos desde nombres de archivo
   - Registro de tiempo de reacción

### 🚧 En Desarrollo

1. **Sistema de triggers ampliado**
   - Triggers específicos por bloque
   - Triggers por tipo de regla
   - Triggers por tipo de estímulo (Single/Double)
   - Triggers de cambio de regla

2. **Almacenamiento de datos**
   - Escritura de CSV con respuestas
   - Inclusión de metadata de reglas
   - Registro de series y transiciones

3. **Análisis post-experimento**
   - Cálculo de perseveraciones
   - Errores de mantenimiento de set
   - Curvas de aprendizaje

---

## Referencias

### Bibliografía

- **Wisconsin Card Sorting Task (WCST)**: Grant, D. A., & Berg, E. A. (1948). A behavioral analysis of degree of reinforcement and ease of shifting to new responses in a Weigl-type card-sorting problem. *Journal of Experimental Psychology*, 38(4), 404-411.

- **Funciones Ejecutivas**: Heaton, R. K., Chelune, G. J., Talley, J. L., Kay, G. G., & Curtiss, G. (1993). *Wisconsin Card Sorting Test Manual: Revised and Expanded*. Psychological Assessment Resources.

### Documentación Técnica

- **Pygame**: https://www.pygame.org/docs/
- **PySerial**: https://pyserial.readthedocs.io/

---

## Contacto y Soporte

Para preguntas, reportar bugs o solicitar nuevas funcionalidades:

- **Email**: [tu_email@institucion.edu]
- **Issues**: [URL del repositorio]/issues
- **Documentación**: [URL de la wiki]

---

## Licencia

[Especificar licencia: MIT, GPL, etc.]

---

## Agradecimientos

- [Nombres de colaboradores]
- [Instituciones participantes]
- [Fuentes de financiamiento]

---

**Última actualización**: 30 de enero de 2026  
**Versión del documento**: 2.0  
**Versión del código**: 0.1  
**Estado**: ✅ Funcional | 🚧 Triggers en desarrollo