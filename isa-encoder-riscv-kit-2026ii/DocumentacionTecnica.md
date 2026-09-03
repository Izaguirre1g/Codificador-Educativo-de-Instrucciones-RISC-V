## 1. Instrucciones soportadas

El codificador implementa las siguientes instrucciones de la arquitectura
RISC-V RV32I:

| Formato | Instrucciones |
|---------|---------------|
| R | add, sub, and, or |
| I | addi, andi, lw, lb |
| S | sw, sb |
| B | beq, bne |

Cada instrucción recibe una cadena de texto con la sintaxis del ensamblador
RISC-V y retorna su codificación correspondiente de 32 bits.

## 2. Obtención de campos de codificación

Los campos utilizados para generar las instrucciones fueron obtenidos del
manual oficial:

RISC-V User-Level ISA Volume I:
Unprivileged ISA (versión 20191213).

Cada instrucción se divide en campos dependiendo del formato utilizado.

### Instruccion tipo R

Utilizado por instrucciones aritméticas entre registros.

La estructura es:

| Campo | Bits |
|-|-|
| funct7 | 31-25 |
| rs2 | 24-20 |
| rs1 | 19-15 |
| funct3 | 14-12 |
| rd | 11-7 |
| opcode | 6-0 |

Ejemplo:
add x5, x6, x7

Se utilizan:
opcode = 0110011
funct3 = 000
funct7 = 0000000


---

### Instruccion tipo I

Utilizado para inmediatos y cargas desde memoria.

Estructura:

| Campo | Bits |
|-|-|
| imm |31-20|
| rs1 |19-15|
| funct3|14-12|
| rd|11-7|
|opcode|6-0|


---

### Instruccion tipo S

Utilizado para instrucciones store.

Estructura:

| Campo | Bits |
|-|-|
| imm[11:5]|31-25|
| rs2 |24-20|
| rs1 |19-15|
| funct3|14-12|
| imm[4:0]|11-7|
| opcode|6-0|


---

### Instruccion tipo B

Utilizado para instrucciones de salto condicional.

Estructura:

| Campo | Bits |
|-|-|
| imm[12]|31|
| imm[10:5]|30-25|
| rs2|24-20|
| rs1|19-15|
| funct3|14-12|
| imm[4:1]|11-8|
| imm[11]|7|
| opcode|6-0|

## 3. Arquitectura del código

El programa está compuesto principalmente por dos funciones:

### encode_instruction()

Esta función recibe una instrucción en formato texto.

Ejemplo:
add x5, x6, x7

Primero realiza un parseo de la cadena para separar:

- mnemónico
- registros fuente
- registro destino
- valores inmediatos


Posteriormente identifica el formato de la instrucción:

- R
- I
- S
- B


Finalmente ensambla los campos mediante operaciones de desplazamiento
de bits (`<<`) y combinación lógica OR (`|`).


Ejemplo:

```python
word = (
    funct7 << 25 |
    rs2 << 20 |
    rs1 << 15 |
    funct3 << 12 |
    rd << 7 |
    opcode
)
El resultado es una palabra de 32 bits almacenada como entero.



---

# 4. Ejemplos de salida explicativa

Aquí debes colocar capturas o texto de 4 instrucciones:

Una por formato:

- R → add
- I → addi
- S → sw
- B → beq

Ejemplo:



## 5. Validación contra herramienta oficial

La validación se realizó utilizando el toolchain oficial RISC-V.

Para cada instrucción se generaron tres casos diferentes,
considerando registros diferentes y valores inmediatos positivos,
negativos y límites.

La comparación se realizó mediante:

- codificación generada por el modelo propio
- codificación obtenida mediante objdump


Ejemplo:

| Instrucción | Modelo | objdump | Resultado |
|-|-|-|-|
| add x5,x6,x7 | 0x007302b3 |0x007302b3|OK|
| addi x10,x1,-12|0xff408513|0xff408513|OK|
| sw x5,8(x6)|0x00532423|0x00532423|OK|
| beq x5,x6,8|0x00628463|0x00628463|OK|


## 6. Instalación del toolchain RISC-V

El proyecto fue validado utilizando el toolchain:

Instalación en Ubuntu:

```bash
sudo apt update

sudo apt install binutils-riscv64-unknown-elf
riscv64-unknown-elf-as --version
riscv64-unknown-elf-objdump --version


---

# 7. Preparación de la herramienta

Aquí explicas cómo correr tu programa:

```markdown
## 7. Preparación y ejecución

Requisitos:

- Python 3
- Ubuntu/Linux
- Toolchain RISC-V instalado


Ejecutar:

```bash
chmod +x run.sh

./run.sh "add x5, x6, x7"
