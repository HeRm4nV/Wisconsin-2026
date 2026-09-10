# Wisconsin Card Sorting Task (WCST) - Protocolo Experimental

## Descripción General

Este experimento implementa una versión adaptada del **Wisconsin Card Sorting Task (WCST)**, una prueba neuropsicológica diseñada para evaluar funciones ejecutivas, flexibilidad cognitiva y capacidad de cambio de set mental.

## Información del Experimento

- **Nombre**: Wisconsin Task
- **Versión**: 1.1.0
- **Python Version**: 3.11
- **Autor**: Herman Valencia
- **Estado**: ✅ Versión estable | ✅ Sistema de Triggers Actualizado

---

## Estructura del Experimento

### Configuración de Bloques

El experimento consta de **4 bloques**. En la versión estable 1.1.0, la distribución de mazos se calcula dinámicamente a partir del tamaño real del mazo (`DECK_SIZE`) y de los ensayos requeridos por bloque.

Cada bloque contiene **108 ensayos** y la continuidad de los mazos se mantiene entre bloques. Por lo tanto, los tamaños concretos de los cortes de mazo pueden variar según dónde haya quedado el mazo anterior.

**Total del experimento**: 432 ensayos (4 bloques × 108 ensayos)

### Estructura de Series

Cada bloque contiene **18 series** con la siguiente distribución:

- **6 series de 5 ensayos** (30 ensayos)
- **6 series de 6 ensayos** (36 ensayos)
- **6 series de 7 ensayos** (42 ensayos)

**Total por bloque**: 108 ensayos

> **Nota**: El orden de las series se aleatoriza en cada bloque para evitar efectos de orden.

---

## Reglas de Clasificación

El experimento utiliza **3 reglas de clasificación** que se presentan en orden balanceado:

### Tipos de Reglas

1. **Número** (`"number"`): Emparejar según la cantidad de elementos
2. **Color** (`"color"`): Emparejar según el color de los elementos
3. **Figura** (`"figure"`): Emparejar según la forma de los elementos

### Distribución de Reglas

- Cada bloque tiene **18 series** (6 iteraciones de las 3 reglas)
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
- **Cantidad disponible**: 24 cartas únicas
- **Ubicación**: `media/images/Single/`
- **Uso en la versión estable**: Cada serie comienza con **3 cartas singles obligatorias**, salvo los casos límite en los que el corte de mazo no dispone de suficientes slots.

### 2. Doubles (Cartas Dobles)
- **Cantidad disponible**: 36 cartas únicas
- **Ubicación**: `media/images/Double/`
- **Uso en la versión estable**: Se utilizan junto con las singles para completar cada serie.

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
- La versión estable utiliza **24 singles + 24 doubles por mazo completo**, para una proporción **1:1 (50:50)**.
- `MAX_TYPE_A = 24` limita las singles disponibles por mazo.
- `MAX_TYPE_B = 36` define el máximo disponible de doubles, aunque la configuración estable limita cada mazo a 24 doubles mediante el cálculo proporcional.
- La configuración anterior 24:36 (40:60) se conserva únicamente en la rama `first_version=True`.

### 2. Sistema de Mazos Múltiples
- El tamaño efectivo del mazo se calcula automáticamente mediante `PERCENTAGE`, `MAX_TYPE_A` y `MAX_TYPE_B`.
- En la versión estable (`first_version=False`), `DECK_SIZE` resulta en **48 cartas**.
- Los bloques no utilizan una lista fija de tamaños: `block_creation()` calcula dinámicamente los cortes necesarios para completar los ensayos de cada bloque.
- Los mazos se consumen secuencialmente a través de las series y la posición restante de un mazo puede continuar en el bloque siguiente.

### 3. Inicialización de Series

Para cada serie:

1. **Reserva proporcional**: Se calculan cuántas singles y doubles se necesitan del mazo actual.
2. **Singles obligatorias**: Se intentan añadir **3 cartas singles** al inicio de cada serie nueva.
3. **Manejo de casos límite**: Si el último corte no dispone de suficientes slots, se añaden únicamente las singles que caben sin sobrellenar la serie.
4. **Mezcla balanceada**: Las singles y doubles restantes se mezclan aleatoriamente.
5. **Relleno de series**: Se completa cada serie hasta su tamaño objetivo.

### 4. Reutilización de Cartas

- Las cartas **no utilizadas** en un mazo se transfieren automáticamente al siguiente.
- Los restos se mantienen mediante `DeckCursor` y se utilizan antes de crear un nuevo mazo.
- Cuando se crea un nuevo mazo, se vuelven a mezclar las listas de singles y doubles y se seleccionan las cantidades calculadas para el mazo.

### 5. Validación Automática

El sistema valida que:
- Cada bloque tenga exactamente `TRIALS_PER_BLOCK` ensayos.
- `TRIALS_PER_BLOCK` se calcula a partir de `SERIES_DISTRIBUTION` y actualmente es **108**.
- No haya series vacías.
- Las series alcancen su tamaño objetivo.
- Las cartas obligatorias disponibles no sean insuficientes.

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

El sistema de triggers de la versión estable está implementado mediante **puerto serial (COM)**.

**Parámetros principales en el código**:
```python
serial_port = "COM5"          # Puerto COM utilizado por main()
trigger_gap = 250             # Tiempo reservado entre secciones de triggers (ms)
individual_trigger_gap = 30   # Separación entre triggers de una misma sección (ms)
start_trigger = 254           # Trigger de inicio
stop_trigger = 255             # Trigger de fin
```

### Tabla Completa de Triggers

#### Triggers de Control del Experimento

| Código | Nombre | Descripción | Momento de Envío |
|--------|--------|-------------|------------------|
| `254` | `start_experiment` | Inicio del experimento | Al comenzar la sesión |
| `255` | `end_experiment` | Fin del experimento | Al finalizar la sesión |
| `70` | `fixation` | Cruz de fijación | Antes de cada ensayo |
| `80` | `stimulus_onset` | Inicio de presentación del estímulo | Inmediatamente antes de mostrar la carta objetivo |
| `90` | `feedback_trigger` | Inicio del feedback visual | Después de mostrar el feedback de la respuesta |

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
7. [80]  → stimulus_onset (inicio de presentación)
8. [22]  → answer_2 (usuario presiona V)
9. [121] → correct_response (respuesta correcta)
10. [141] → first_correct (primera correcta de la serie)
11. [90] → feedback_trigger (inicio del feedback visual)
```

**Ejemplo: Último ensayo de una serie (respuesta correcta)**

```
1. [70]  → fixation
2. [235] → last_target_card (última carta de la serie)
3. [32]  → red_card
4. [42]  → triangle_card
5. [51]  → number_1_card
6. [80]  → stimulus_onset
7. [21]  → answer_1
8. [121] → correct_response
9. [181] → other_correct (tercera o más correcta)
10. [230] → last_feedback_181 (feedback final de serie)
11. [90] → feedback_trigger
```

### Integración Hardware

#### Puerto Serial (COM)

La versión estable utiliza la interfaz serial mediante `pyserial`.

```python
init_com(address="COM3")
send_trigger(trigger)
close_com()
```

**Configuración**:
- **Baudrate**: 115200
- **Formato**: 1 byte por trigger
- **Puerto por defecto de `init_com()`**: COM3
- **Puerto utilizado por `main()`**: COM5, definido en `serial_port`

> **Nota**: La versión estable actual no implementa una función `init_lpt()` ni `send_trigger_lpt()`. El código fuente contiene únicamente la implementación de triggers por puerto serial.

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

1. **Activar modo debug**: `debug = True` en `Wisconsin.py`
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
Serie 18: Tamaño 7

Distribución de mazos:
  Mazo 1 (tamaño variable): series 1 a ...
    Serie 1: usa 7 slots
    Serie 2: usa 6 slots
    ...
  Mazo 2 (tamaño variable): continuación según el corte calculado
    ...
```

#### 2. Archivo de Datos Experimentales

La versión estable genera un archivo CSV por sesión con las siguientes columnas:

| Campo | Descripción |
|-------|-------------|
| `Sujeto` | ID del participante |
| `IdImagen` | Nombre del archivo de la carta |
| `Bloque` | Número de bloque (1-4) |
| `TReaccion` | Tiempo de reacción en ms |
| `TipoSerie` | Regla activa (number/color/figure) |
| `Respuesta` | Índice de respuesta seleccionada (0=C, 1=V, 2=B, 3=N) |
| `Acierto` | 1 si correcto, 0 si incorrecto |

El nombre del archivo sigue el formato:

```text
[ID]_pre_Wisconsin_YYYY-MM-DD_HH-MM-SS.csv
[ID]_post_Wisconsin_YYYY-MM-DD_HH-MM-SS.csv
```

La condición se solicita al inicio de la sesión:
- `1`: Registro previo a dosificación (`_pre`)
- `2`: Registro posterior a dosificación (`_post`)

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

**Para Puerto Serial**:
1. Identificar el puerto COM disponible.
2. Modificar `serial_port` en el código si es necesario.
3. La función `main()` inicializa la conexión mediante `init_com(address=serial_port)`.

### 5. Ejecutar el Experimento

```bash
python "Wisconsin.py"
```

---

## Modo Debug

### Activación

La versión estable ya inicia con:

```python
debug = True
```

Puede cambiarse a `False` en `Wisconsin.py` para ejecutar con salida mínima.

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
   - Cada bloque debe tener exactamente 108 ensayos
   - Error si la suma de mazos ≠ `TRIALS_PER_BLOCK`

2. **Proporción Singles/Doubles**
   - La configuración estable utiliza 24 singles y 24 doubles por mazo completo
   - Proporción efectiva 50:50

3. **Series Completas**
   - Todas las series deben alcanzar su tamaño objetivo
   - No se permiten series incompletas

4. **Singles Obligatorias**
   - Cada serie intenta comenzar con 3 singles
   - En cortes límite se utilizan solo las singles que caben sin sobrellenar

5. **Reglas Balanceadas**
   - 6 repeticiones de cada regla por bloque
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

### Error: "Not enough Singles for mandatory 3 per series"

**Causa**: No hay suficientes singles disponibles para completar las 3 singles obligatorias de una serie.

**Solución**: Verificar que existan las 24 imágenes de `media/images/Single/` y que el estado del `DeckCursor` permita disponer de las singles necesarias.

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

**Causa**: Puerto serial no inicializado, puerto COM incorrecto o configuración incorrecta.

**Solución**:
1. Verificar que `init_com(address=serial_port)` se ejecute al inicio.
2. Comprobar el mensaje de consola: "Serial port opened".
3. Verificar que `serial_port` corresponda al puerto COM utilizado por el sistema.
4. Utilizar `serial.tools.list_ports` para comprobar los puertos disponibles.

### Triggers Duplicados o Perdidos

**Causa**: Separación insuficiente entre triggers o problemas de sincronización.

**Solución**:
1. Revisar `individual_trigger_gap` (30 ms por defecto).
2. Revisar `trigger_gap` (250 ms por defecto).
3. Usar `sleepy_trigger()` cuando se requiera una espera explícita después del envío.
4. Verificar que el sistema EEG pueda procesar triggers rápidos.

---

## Notas Importantes

### 1. Aleatorización
- Las cartas singles y doubles se aleatorizan **una vez** al inicio de la sesión
- Las reglas de clasificación se aleatorizan por iteración (cada 3 series)
- Los tamaños de series se aleatorizan por bloque

### 2. Continuidad de Mazos
- Las cartas sobrantes de un mazo se **reutilizan automáticamente** en el siguiente.
- La continuidad puede extenderse al siguiente bloque cuando el mazo actual no termina exactamente al final del bloque.
- Los mazos nuevos se construyen con 24 singles y 24 doubles.

### 3. Reglas de Clasificación
- **No se repite** la misma regla entre el final de una iteración y el inicio de la siguiente
- Esto garantiza cambios de set mental claros
- El participante debe inferir la regla activa mediante retroalimentación

### 4. Tiempo de Respuesta
- **No hay límite de tiempo** para responder
- Se registra el tiempo de reacción desde la presentación del estímulo
- Se recomienda responder lo más rápido posible

### 5. Archivos Debug
- Los archivos ZIP se generan **automáticamente** en cada sesión con `debug=True`.
- La versión estable inicia con `debug=True`.
- **No se sobreescriben**: cada sesión tiene su propio timestamp.
- Además, `block_creation()` imprime la estructura generada cuando el modo debug está activo.
- Son útiles para validar la estructura del experimento antes de recopilar datos.

### 6. Sistema de Triggers
- Los triggers se envían de forma **síncrona** con los eventos visuales.
- `trigger_gap` se establece en 250 ms y `individual_trigger_gap` en 30 ms por defecto.
- Todos los triggers importantes se documentan en la consola (modo debug).
- La versión estable utiliza puerto serial (COM).

### 7. Nomenclatura de Archivos
- **Crítico**: Los nombres de archivos deben seguir el formato exacto
- Formato: `[numero]_[figura]_[color].png`
- El sistema extrae atributos directamente del nombre del archivo
- Nombres incorrectos causarán errores de validación

---

## Cambios en Versión 1.1.0

### ✅ Nuevo en esta Versión

La versión **1.1.0** reemplaza la configuración anterior y queda establecida como la versión que se utilizará de ahora en adelante.

1. **Nueva estructura de series**
   - Se pasa de **15 a 18 series por bloque**.
   - La distribución anterior de 6, 7 y 8 ensayos se reemplaza por:
     - 6 series de 5 ensayos.
     - 6 series de 6 ensayos.
     - 6 series de 7 ensayos.
   - Cada bloque pasa de **105 a 108 ensayos**.
   - El experimento completo pasa de **420 a 432 ensayos**.

2. **Nueva configuración de mazos**
   - La configuración estable utiliza `first_version = False`.
   - Se definen `MAX_TYPE_A = 24` y `MAX_TYPE_B = 36` como límites de cartas disponibles.
   - La proporción estable pasa a **1:1** mediante `PERCENTAGE = [1, 1]`.
   - El tamaño efectivo de un mazo nuevo pasa a **48 cartas: 24 singles + 24 doubles**.
   - La rama `first_version=True` se mantiene en el código como configuración usable, pero no es la seleccionada en la versión estable.

3. **Generación dinámica de cortes de mazo**
   - `block_creation()` ya no depende de una lista fija de `deck_sizes_per_block`.
   - Los cortes se calculan automáticamente a partir de `DECK_SIZE` y `TRIALS_PER_BLOCK`.
   - La posición restante de un mazo se conserva entre cortes y puede continuar entre bloques.
   - Esto permite que los bloques utilicen cortes variables sin modificar manualmente la estructura.

4. **Aumento de singles obligatorias**
   - `MANDATORY_SINGLES_PER_SERIES` establece **3 singles obligatorias por serie**.
   - `initialize_series()` ahora utiliza este valor en lugar de tener el número 2 fijado directamente.
   - Se amplió el manejo de casos límite del último corte para añadir solo las singles que caben sin sobrellenar la serie.

5. **Mejora del control y depuración de mazos**
   - Se imprime el estado de `DeckCursor` antes de cada corte cuando `debug=True`.
   - Se muestra información adicional al iniciar cada mazo.
   - Se imprime la estructura completa de `block_stacks` al finalizar `block_creation()` en modo debug.
   - Se mantienen los archivos `debug_blocks_structure.txt` y `debug_block_X.txt` dentro del ZIP de depuración.

6. **Generación de tipos de serie adaptable**
   - `generate_series_types_for_block()` deja de asumir 15 series.
   - Utiliza `SERIES_PER_BLOCK` para determinar cuántas series debe generar.
   - Con la configuración estable, genera **18 reglas por bloque**, con **6 series de cada regla**.
   - Se mantiene la restricción de que la primera regla de una nueva iteración no sea igual a la última de la iteración anterior.

7. **Bloque de práctica adaptable**
   - `trial_block_creation()` ya no utiliza exclusivamente el intervalo fijo 6-8.
   - El tamaño de las series de práctica se obtiene mediante el mínimo y máximo de `SERIES_DISTRIBUTION`.
   - Con la configuración estable, las series de práctica pueden tener entre **5 y 7 ensayos**.

8. **Versión del experimento**
   - `EXPERIMENT_VERSION` pasa de `"0.1"` a `"1.1.0"`.
   - La documentación se actualiza para identificar **1.1.0** como la versión estable actual.

9. **Modo debug por defecto**
   - `debug` pasa de `False` a `True`.
   - La ejecución estable proporciona información de depuración y genera los archivos de validación automáticamente.

10. **Trazabilidad de triggers**
    - Se mantiene el sistema de triggers existente.
    - Se documentan explícitamente los triggers `80` (`stimulus_onset`) y `90` (`feedback_trigger`), utilizados para sincronizar la presentación del estímulo y del feedback.
    - La secuencia documentada de triggers se actualiza para reflejar estos eventos.

11. **Registro de datos**
    - El CSV generado por la versión estable queda documentado según las **7 columnas que realmente escribe el código**.
    - El nombre del archivo incorpora la condición `_pre` o `_post` y el timestamp de la sesión.

### 🔄 Diferencias principales respecto a la versión anterior

| Característica | Versión anterior | Versión estable 1.1.0 |
|----------------|------------------|------------------------|
| Series por bloque | 15 | 18 |
| Distribución de series | 5×6, 5×7, 5×8 | 6×5, 6×6, 6×7 |
| Ensayos por bloque | 105 | 108 |
| Ensayos totales | 420 | 432 |
| Proporción por mazo | 24 singles : 36 doubles (40:60) | 24 singles : 24 doubles (50:50) |
| Tamaño de mazo nuevo | 60 | 48 |
| Singles obligatorias | 2 | 3 |
| Cortes de mazo | Definidos manualmente | Calculados dinámicamente |
| Continuidad de mazos | Entre cortes del bloque | Entre cortes y, cuando corresponde, entre bloques |
| Tipos de regla por bloque | 15 | 18 |
| Repeticiones de cada regla | 5 | 6 |
| Modo debug inicial | `False` | `True` |
| Versión del código | `0.1` | `1.1.0` |

### ⚠️ Configuración histórica conservada

- `first_version = True` conserva la configuración anterior dentro del código:
  - Series de 6, 7 y 8 ensayos.
  - 15 series por bloque.
  - 105 ensayos por bloque.
  - Proporción 2:3.
- **No modificar `first_version` a `True` para la ejecución estable**, ya que la configuración oficial de trabajo es `first_version = False`.

### 🔧 Cambios de implementación relevantes

- `block_creation()` ahora calcula `deck_sizes_per_block` internamente.
- `initialize_series()` utiliza `MANDATORY_SINGLES_PER_SERIES` y maneja de forma general los casos límite del último corte.
- `trial_block_creation()` obtiene los límites de tamaño desde `SERIES_DISTRIBUTION`.
- `generate_series_types_for_block()` utiliza `SERIES_PER_BLOCK`.
- `main()` conserva el flujo experimental, pero ahora puede mostrar la estructura completa de bloques en modo debug.

---

## Referencias

### Bibliografía

- **Wisconsin Card Sorting Task (WCST)**: Grant, D. A., & Berg, E. A. (1948). A behavioral analysis of degree of reinforcement and ease of shifting to new responses in a Weigl-type card-sorting problem. *Journal of Experimental Psychology*, 38(4), 404-411.

- **Funciones Ejecutivas**: Heaton, R. K., Chelune, G. J., Talley, J. L., Kay, G. G., & Curtiss, G. (1993). *Wisconsin Card Sorting Test Manual: Revised and Expanded*. Psychological Assessment Resources.

- **Marcadores EEG**: Duncan-Johnson, C. C., & Donchin, E. (1977). On quantifying surprise: The variation of event-related potentials with subjective probability. *Psychophysiology*, 14(5), 456-467.

### Documentación Técnica

- **Pygame**: https://www.pygame.org/docs/
- **PySerial**: https://pyserial.readthedocs.io/

---

## Contacto y Soporte

Para preguntas, reportar bugs o solicitar nuevas funcionalidades:

- **Email**: herman.valencia.inf@gmail.com
- **Issues**: https://github.com/HeRm4nV/Wisconsin-2026/issues
- **Documentación**: Ver `Wisconsin.py` para detalles de implementación

---

**Última actualización**: 10 de septiembre de 2026  
**Versión del documento**: 3.2  
**Versión del código**: 1.1.0  
**Versión del experimento**: 1.1.0  
**Estado**: ✅ Versión estable | ✅ Triggers documentados y actualizados