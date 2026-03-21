# Wisconsin Card Sorting Task (WCST) - Protocolo Experimental

## Descripción General

Este experimento implementa una versión adaptada del **Wisconsin Card Sorting Task (WCST)**, una prueba neuropsicológica diseñada para evaluar funciones ejecutivas, flexibilidad cognitiva y capacidad de cambio de set mental.

## Información del Experimento

- **Nombre**: Wisconsin Task
- **Versión**: 1.1
- **Python Version**: 3.11
- **Autor**: Herman Valencia
- **Estado**: ✅ Funcional | ✅ Sistema de Triggers Actualizado

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
| 1 (Izquierda) | **C** | Triángulo rojo | `1_triangle_red.png` |
| 2 | **V** | Dos estrellas verdes | `2_star_green.png` |
| 3 | **B** | Tres cruces amarillas | `3_cross_yellow.png` |
| 4 (Derecha) | **N** | Cuatro círculos azules | `4_circle_blue.png` |

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

**Ejemplo**: `1_triangle_red.png`, `2_star_green.png`, `3_cross_yellow.png`

**Valores válidos**:
- **Número**: `1`, `2`, `3`, `4`
- **Figura**: `triangle`, `star`, `cross`, `circle`
- **Color**: `red`, `green`, `yellow`, `blue`

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
   - **Trigger enviado**: `70` (fixation)

2. **Presentación del Estímulo**
   - Se muestra la carta objetivo en el centro inferior
   - Las 4 cartas de referencia permanecen visibles arriba
   - El participante responde usando las teclas **C**, **V**, **B**, o **N**
   - **Triggers enviados**:
     - Color de la carta: `31`-`34`
     - Figura de la carta: `41`-`44`
     - Número de elementos: `51`-`54`
     - Primer estímulo de la serie: `60` (solo en el primer ensayo)
     - Regla activa: `11` (number), `12` (figure), o `13` (color)
     - Última carta de la serie: `235` (solo en el último ensayo)

3. **Registro de Respuesta**
   - **Trigger enviado**: `21`-`24` según tecla presionada (C=21, V=22, B=23, N=24)

4. **Retroalimentación** (1500 ms)
   - **Correcto**: ✓ verde en el centro de la pantalla
   - **Incorrecto**: ✗ roja en el centro de la pantalla
   - **Triggers enviados**:
     - Respuesta correcta: `121`
     - Respuesta incorrecta: `102`
     - Posición en secuencia de aciertos/errores:
       - Primera correcta: `141`
       - Segunda correcta: `161`
       - Otra correcta: `181`
       - Primer error: `104`
       - Segundo error: `106`
       - Otro error: `108`
       - Error entre correctas: `110`
     - Feedback de última carta (solo en último ensayo de serie):
       - `205`, `210`, `215` (errores)
       - `220`, `225`, `230` (aciertos)

### Descansos Entre Bloques

```
Fin del bloque [N].

Tómate de 2 a 3 minutos para descansar.

Cuando estés lista/o para continuar presiona la barra espaciadora.
```

- **Trigger al final de cada bloque**: `10`, `20`, `30`, `40` (según bloque)

### Finalización

```
La tarea ha finalizado.

Muchas gracias por su colaboración!!
```

- **Trigger de fin de experimento**: `255`

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

### Configuración del Sistema

El sistema de triggers está implementado y soporta tanto puerto paralelo (LPT) como puerto serial (COM).

**Parámetros en el código**:
```python
lpt_address = 0xD100       # Dirección del puerto paralelo
trigger_latency = 5        # Latencia en milisegundos
start_trigger = 254        # Trigger de inicio
stop_trigger = 255         # Trigger de fin
```

### Tabla Completa de Triggers

#### Triggers de Control del Experimento

| Código | Nombre | Descripción | Momento de Envío |
|--------|--------|-------------|------------------|
| `254` | `start_experiment` | Inicio del experimento | Al comenzar la sesión |
| `255` | `end_experiment` | Fin del experimento | Al finalizar la sesión |
| `70` | `fixation` | Cruz de fijación | Antes de cada ensayo |

#### Triggers de Bloques

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `1` | `block_1_start` | Inicio del bloque 1 |
| `2` | `block_2_start` | Inicio del bloque 2 |
| `3` | `block_3_start` | Inicio del bloque 3 |
| `4` | `block_4_start` | Inicio del bloque 4 |
| `10` | `block_1_end` | Fin del bloque 1 |
| `20` | `block_2_end` | Fin del bloque 2 |
| `30` | `block_3_end` | Fin del bloque 3 |
| `40` | `block_4_end` | Fin del bloque 4 |

#### Triggers de Series

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `60` | `first_stimulus_per_serie` | Primer estímulo de cada serie |
| `235` | `last_target_card` | Última carta objetivo de la serie |

#### Triggers de Reglas Activas

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `11` | `actual_rule_number` | Regla activa: Número |
| `12` | `actual_rule_figure` | Regla activa: Figura |
| `13` | `actual_rule_color` | Regla activa: Color |

#### Triggers de Atributos de Cartas - Color

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `31` | `blue_card` | Carta con elementos azules |
| `32` | `red_card` | Carta con elementos rojos |
| `33` | `green_card` | Carta con elementos verdes |
| `34` | `yellow_card` | Carta con elementos amarillos |

#### Triggers de Atributos de Cartas - Figura

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `41` | `star_card` | Carta con estrellas |
| `42` | `triangle_card` | Carta con triángulos |
| `43` | `cross_card` | Carta con cruces |
| `44` | `circle_card` | Carta con círculos |

#### Triggers de Atributos de Cartas - Número

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `51` | `number_1_card` | Carta con 1 elemento |
| `52` | `number_2_card` | Carta con 2 elementos |
| `53` | `number_3_card` | Carta con 3 elementos |
| `54` | `number_4_card` | Carta con 4 elementos |

#### Triggers de Respuestas del Participante

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `21` | `answer_1` | Respuesta: Tecla C (carta 1) |
| `22` | `answer_2` | Respuesta: Tecla V (carta 2) |
| `23` | `answer_3` | Respuesta: Tecla B (carta 3) |
| `24` | `answer_4` | Respuesta: Tecla N (carta 4) |

#### Triggers de Evaluación de Respuestas

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `121` | `correct_response` | Respuesta correcta |
| `102` | `incorrect_response` | Respuesta incorrecta |

#### Triggers de Secuencias de Aciertos

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `141` | `first_correct` | Primera respuesta correcta consecutiva |
| `161` | `second_correct` | Segunda respuesta correcta consecutiva |
| `181` | `other_correct` | Tercera o más respuestas correctas consecutivas |

#### Triggers de Secuencias de Errores

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `104` | `first_error` | Primer error consecutivo |
| `106` | `second_error` | Segundo error consecutivo |
| `108` | `other_error` | Tercer o más errores consecutivos |
| `110` | `error_between_correct` | Error después de respuestas correctas |

#### Triggers de Feedback Final de Serie

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `205` | `last_feedback_104` | Feedback del último ensayo (primer error) |
| `210` | `last_feedback_106` | Feedback del último ensayo (segundo error) |
| `215` | `last_feedback_108` | Feedback del último ensayo (otros errores) |
| `220` | `last_feedback_141` | Feedback del último ensayo (primera correcta) |
| `225` | `last_feedback_161` | Feedback del último ensayo (segunda correcta) |
| `230` | `last_feedback_181` | Feedback del último ensayo (otras correctas) |

### Secuencia Típica de Triggers por Ensayo

**Ejemplo: Primer ensayo de una serie nueva (regla = color, carta = 2 estrellas verdes)**

```
1. [70]  → fixation (cruz de fijación)
2. [60]  → first_stimulus_per_serie (primer estímulo)
3. [13]  → actual_rule_color (regla activa: color)
4. [33]  → green_card (carta verde)
5. [41]  → star_card (carta con estrellas)
6. [52]  → number_2_card (carta con 2 elementos)
7. [22]  → answer_2 (usuario presiona V)
8. [121] → correct_response (respuesta correcta)
9. [141] → first_correct (primera correcta de la serie)
```

**Ejemplo: Último ensayo de una serie (respuesta correcta)**

```
1. [70]  → fixation
2. [235] → last_target_card (última carta de la serie)
3. [32]  → red_card
4. [42]  → triangle_card
5. [51]  → number_1_card
6. [21]  → answer_1
7. [121] → correct_response
8. [181] → other_correct (tercera o más correcta)
9. [230] → last_feedback_181 (feedback final de serie)
```

### Integración Hardware

#### Puerto Paralelo (LPT)

```python
init_lpt(address=0xD100)
send_trigger(trigger, address, latency=5)
```

**Requisitos**:
- Sistema operativo Windows
- Archivo [`dlportio.dll`](https://real.kiev.ua/avreal/download/) instalado
- Permisos de administrador

**Instalación de dlportio.dll**:
1. Descargar desde el enlace oficial
2. Copiar a:
   - `C:\Windows\System32\` (Windows 64-bit)
   - `C:\Windows\SysWOW64\` (Windows 32-bit)
3. Ejecutar el programa como Administrador

#### Puerto Serial (COM)

```python
init_com(address="COM3")
send_trigger(trigger)
close_com()
```

**Configuración**:
- **Baudrate**: 115200
- **Formato**: 1 byte por trigger
- **Puerto por defecto**: COM3

**Verificar puertos disponibles**:
```python
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)
```

### Función de Trigger con Latencia

```python
sleepy_trigger(trigger, latency=100)
```

Esta función envía un trigger y espera la latencia especificada antes de continuar, útil para asegurar la recepción del trigger por el sistema EEG.

### Validación de Triggers

Para verificar que los triggers se envían correctamente:

1. **Activar modo debug**: `debug = True` en [`home version.py`](home%20version.py)
2. Los mensajes de consola mostrarán cada trigger enviado:
   ```
   Trigger 70 sent
   Trigger 60 sent
   Trigger 13 sent
   ...
   ```

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

#### 2. Archivo de Datos Experimentales (En Desarrollo)

**Formato CSV planeado** con las siguientes columnas:

| Campo | Descripción |
|-------|-------------|
| `Sujeto` | ID del participante |
| `IdImagen` | Nombre del archivo de la carta |
| `Bloque` | Número de bloque (1-4) |
| `Serie` | Número de serie dentro del bloque (1-15) |
| `Ensayo` | Número de ensayo dentro de la serie |
| `TipoRegla` | Regla activa (number/color/figure) |
| `TReaccion` | Tiempo de reacción en ms |
| `TipoImagen` | Single o Double |
| `ColorCarta` | Color de la carta (red/green/yellow/blue) |
| `FiguraCarta` | Figura de la carta (triangle/star/cross/circle) |
| `NumeroCarta` | Número de elementos (1/2/3/4) |
| `Respuesta` | Tecla presionada (0=C, 1=V, 2=B, 3=N) |
| `Acierto` | 1 si correcto, 0 si incorrecto |
| `SecuenciaAciertos` | Contador de aciertos consecutivos |
| `SecuenciaErrores` | Contador de errores consecutivos |

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
├── [numero]_[figura]_[color].png
├── ...
└── [numero]_[figura]_[color].png
```

**Doubles** (36 archivos requeridos):
```
media/images/Double/
├── [numero]_[figura]_[color].png
├── ...
└── [numero]_[figura]_[color].png
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

**Contenido de [`requirements.txt`](requirements.txt)**:
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

### 4. Configurar Hardware EEG (Opcional)

**Para Puerto Paralelo**:
1. Instalar `dlportio.dll`
2. Verificar dirección del puerto: `lpt_address = 0xD100`
3. Ejecutar como Administrador

**Para Puerto Serial**:
1. Identificar puerto COM disponible
2. Modificar en código si es necesario: `init_com(address="COM3")`

### 5. Ejecutar el Experimento

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
   - **Todos los triggers enviados**

2. **Archivos de Validación**
   - Generación automática de ZIP en `debug_data/`
   - Estructura completa de bloques
   - Listado de todas las cartas por serie

3. **Controles Adicionales**
   - `P`: Saltar bloque actual
   - `ESC`: Salir en cualquier momento (modo debug)

4. **Información de Respuestas**
   ```python
   print(serie_count, image_count)  # Posición actual
   print(series_type)                # Regla activa
   print(correct_answer)             # Respuesta correcta
   print(static_images_list)         # Cartas de referencia
   ```

5. **Triggers Visibles**
   - Cada trigger enviado se imprime en consola
   - Formato: `Trigger [código] sent`
   - Útil para depuración de sincronización EEG

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

5. **Reglas Balanceadas**
   - 5 repeticiones de cada regla por bloque
   - No repetición entre fin e inicio de iteraciones

### Verificación Manual

Usar los archivos de debug para verificar:

```bash
# Extraer y revisar el ZIP más reciente
cd debug_data
unzip debug_blocks_[fecha].zip -d temp/
cat temp/debug_blocks_structure.txt
```

### Validación de Triggers

Para validar que los triggers se envíen correctamente:

1. Ejecutar en modo debug
2. Revisar la consola para cada trigger enviado
3. Usar un sistema de prueba EEG para verificar recepción
4. Comparar timestamps con eventos esperados

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
1. Descargar `dlportio.dll` de: https://real.kiev.ua/avreal/download/
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

### Triggers No Se Envían

**Causa**: Puerto no inicializado o configuración incorrecta

**Solución**:
1. Verificar que `init_lpt()` o `init_com()` se llamen al inicio
2. Comprobar mensajes de consola: "Parallel/Serial port opened"
3. Verificar latencia: `trigger_latency = 5`
4. Probar con diferentes direcciones de puerto

### Triggers Duplicados o Perdidos

**Causa**: Latencia insuficiente o problemas de sincronización

**Solución**:
1. Aumentar `trigger_latency` a 10-20 ms
2. Usar `sleepy_trigger()` en lugar de `send_trigger()` directo
3. Verificar que el sistema EEG pueda procesar triggers rápidos

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

### 6. Sistema de Triggers
- Los triggers se envían de forma **síncrona** con los eventos visuales
- La latencia de 5ms se usa por defecto (ajustable)
- Todos los triggers importantes se documentan en la consola (modo debug)
- El sistema soporta tanto puerto paralelo como serial

### 7. Nomenclatura de Archivos
- **Crítico**: Los nombres de archivos deben seguir el formato exacto
- Formato: `[numero]_[figura]_[color].png`
- El sistema extrae atributos directamente del nombre del archivo
- Nombres incorrectos causarán errores de validación

---

## Cambios en Versión 1.1

### ✅ Nuevo en esta Versión

1. Documentación y consolidación del sistema de triggers (códigos y ejemplos).
2. Mejora de trazabilidad en modo debug: impresión de todos los triggers y detalle de bloques.
3. Se documenta soporte LPT y COM, recomendaciones de latencia y uso de sleepy_trigger.
4. Actualización de la versión del experimento en README a 1.1.
5. Corrección en el manejo de series: la función initialize_series fue actualizada en el código para solucionar el caso límite en el que **solo queda una carta disponible para la última serie de un mazo** — ahora se añade únicamente 1 single cuando corresponde y se ajusta el contador interno para evitar sobrellenados o desbordes.

### 🚧 Notas detectadas / recomendaciones relacionadas con el código fuente

- Implementación de triggers:
  - En versiones previas había observaciones sobre duplicidad de funciones `send_trigger`. En la versión actual del código solo existe la implementación por serial (`init_com` / `send_trigger` por COM). Si se desea soporte LPT directo, se recomienda implementar una función dedicada `send_trigger_lpt(...)` o encapsular ambas implementaciones en un handler que seleccione la interfaz activa.
- `EXPERIMENT_VERSION` en el código actualmente está definido como `"0.1"`. Si la versión del código debe corresponder a la versión del experimento (1.1), actualizar en `home version.py`:
  ```python
  EXPERIMENT_VERSION = "1.1"
  ```
- `create_debug_zip(debug_base_dir, zip_name)`:
  - En la implementación actual `zip_path = debug_base_dir / zip_name` y en la llamada se pasa un Path absoluto para `zip_name` (`DEBUG_DIR / "debug_blocks_...zip"`). Revisar la firma y la construcción de la ruta para evitar crear rutas incorrectas; se sugiere usar: `zip_path = Path(zip_name)` si `zip_name` ya es absoluto, o pasar solo el nombre de archivo y construir la ruta con `DEBUG_DIR`.
- `initialize_series`:
  - Se actualizó para manejar el caso borde en que solo queda una imagen para la última serie del mazo (ver punto 5 en "Nuevo en esta Versión"). Mantener pruebas en modo debug para verificar comportamiento en mazos con divisiones que dejan 1 carta sobrante.
- Revisar contadores y lógica de índices en `initialize_series` y `build_deck_plan` si se observan comportamientos anómalos en casos límite (p. ej. series al límite entre mazos).

Estas observaciones se añaden para mantener coherencia entre documentación y código. Corregir en el código solo si se desea cambiar el comportamiento actual.

---

## Referencias

### Bibliografía

- **Wisconsin Card Sorting Task (WCST)**: Grant, D. A., & Berg, E. A. (1948). A behavioral analysis of degree of reinforcement and ease of shifting to new responses in a Weigl-type card-sorting problem. *Journal of Experimental Psychology*, 38(4), 404-411.

- **Funciones Ejecutivas**: Heaton, R. K., Chelune, G. J., Talley, J. L., Kay, G. G., & Curtiss, G. (1993). *Wisconsin Card Sorting Test Manual: Revised and Expanded*. Psychological Assessment Resources.

- **Marcadores EEG**: Duncan-Johnson, C. C., & Donchin, E. (1977). On quantifying surprise: The variation of event-related potentials with subjective probability. *Psychophysiology*, 14(5), 456-467.

### Documentación Técnica

- **Pygame**: https://www.pygame.org/docs/
- **PySerial**: https://pyserial.readthedocs.io/
- **DLPortIO**: https://real.kiev.ua/avreal/download/

---

## Contacto y Soporte

Para preguntas, reportar bugs o solicitar nuevas funcionalidades:

- **Email**: herman.valencia.inf@gmail.com
- **Issues**: https://github.com/HeRm4nV/Wisconsin-2026/issues
- **Documentación**: Ver [`home version.py`](home%20version.py) para detalles de implementación

---

**Última actualización**: 21 de marzo de 2026  
**Versión del documento**: 3.1  
**Versión del código**: 1.1  
**Versión del experimento**: 1.1  
**Estado**: ✅ Funcional | ✅ Triggers documentados y actualizados