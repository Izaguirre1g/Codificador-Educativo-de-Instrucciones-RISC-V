#!/usr/bin/env python3
"""
Esqueleto del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

Este esqueleto ya implementa el contrato de línea de comandos y de salida
requerido por la especificación. Usted debe completar las dos funciones
marcadas con TODO; puede modificar el resto del archivo si lo necesita,
siempre que se preserve el contrato de invocación y la línea "HEX: 0x...".

No es obligatorio usar este esqueleto ni Python: puede implementar su
propia herramienta desde cero, en el lenguaje que prefiera, siempre que
respete el mismo contrato (ver especificación, sección "Modo de operación").
"""
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]


def encode_instruction(instruction: str) -> int:
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y debe
    retornar su codificación de 32 bits como entero (0 <= valor < 2**32).

    Debe soportar únicamente las instrucciones en SOPORTADAS. Los valores
    de opcode/funct3/funct7 de cada una NO se proveen aquí: deben
    investigarse en el manual oficial de la ISA RISC-V (ver referencia en
    la especificación) y documentarse en el README.
    """
    # TODO: implementar. Sugerencia: parsear el mnemónico y los operandos,
    # despachar según el formato (R/I/S/B), y ensamblar los campos con
    # operaciones de bits.

    #Aquí se parsea la instrucción en partes: mnemónico y operandos
    """
    Va a tomar la instrucción y va a dividir donde se presenten los casos de comas y espacios para 
    así luego identificar los campos de la instrucción y poder codificarlos en binario.
        Por ejemplo, si la instrucción es "add x5, x6, x7", se va a dividir en:
        [
            "add",
            "x5",
            "x6",
            "x7"    
        ]
    
    """
    partes_instruccion = instruction.replace(","," ").split();

    mnemonico = partes_instruccion[0]
    #Instrucciones de formato R: add, sub, and, or
    if mnemonico in ["add", "sub", "and", "or"]:
        #Formato R
        rd = int(partes_instruccion[1][1:])  # Quitar la 'x' y convertir a entero
        rs1 = int(partes_instruccion[2][1:])
        rs2 = int(partes_instruccion[3][1:])

        # Aquí se definen los valores de opcode, funct3 y funct7 según el mnemónico
        if mnemonico == "add":
            opcode = 0b0110011
            funct3 = 0b000
            funct7 = 0b0000000
        elif mnemonico == "sub":
            opcode = 0b0110011
            funct3 = 0b000
            funct7 = 0b0100000
        elif mnemonico == "and":
            opcode = 0b0110011
            funct3 = 0b111
            funct7 = 0b0000000
        elif mnemonico == "or":
            opcode = 0b0110011
            funct3 = 0b110
            funct7 = 0b0000000

        # Ensamblar la instrucción en formato R
        word = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return word
    #Instrucciones de formato I: addi, andi, lw, lb
    if mnemonico in ["addi", "andi"]:
        #Formato I
        rd = int(partes_instruccion[1][1:])  # Quita la 'x' y convertir a entero
        rs1 = int(partes_instruccion[2][1:])
        imm = int(partes_instruccion[3])  # Inmediato
        
        if mnemonico == "addi":
            opcode = 0b0010011
            funct3 = 0b000
        elif mnemonico == "andi":
            opcode = 0b0010011
            funct3 = 0b111
        
        imm = imm & 0xFFF  # Asegura que el inmediato sea de 12 bits
        
        # Ensamblar la instrucción en formato I
        word = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return word

    #Instrucciones de formato I para load: lw, lb
    if mnemonico in ["lw", "lb"]:
        #Formato I para load
        rd = int(partes_instruccion[1][1:])  # Quita la 'x' y convertir a entero
        offset_base = partes_instruccion[2]
        offset, base = offset_base.split('(')
        base = base[:-1]  # Quita el paréntesis de cierre
        rs1 = int(base[1:])  # Quita la 'x' y convertir a entero
        imm = int(offset)  # Inmediato
        
        if mnemonico == "lw":
            opcode = 0b0000011
            funct3 = 0b010
        elif mnemonico == "lb":
            opcode = 0b0000011
            funct3 = 0b000
        
        imm = imm & 0xFFF  # Asegura que el inmediato sea de 12 bits
        
        # Ensamblar la instrucción en formato I
        word = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return word           
    #Instrucciones de formato S: sw, sb
    if mnemonico in ["sw", "sb"]:
        #Formato S para store
        rs2 = int(partes_instruccion[1][1:])  # Quita la 'x' y convertir a entero
        offset_base = partes_instruccion[2]
        offset, base = offset_base.split('(')
        base = base[:-1]  # Quita el paréntesis de cierre
        rs1 = int(base[1:])  # Quita la 'x' y convertir a entero
        imm = int(offset)  # Inmediato
        
        if mnemonico == "sw":
            opcode = 0b0100011
            funct3 = 0b010
        elif mnemonico == "sb":
            opcode = 0b0100011
            funct3 = 0b000
        
        imm = imm & 0xFFF  # Asegura que el inmediato sea de 12 bits
        
        # Ensamblar la instrucción en formato S
        imm_11_5 = (imm >> 5) & 0x7F #Inmediato de 7 bits (11-5) alto
        imm_4_0 = imm & 0x1F #Inmediato de 5 bits (4-0) bajo
        
        word = (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
        return word

    #Instrucciones de formato B: beq, bne
    if mnemonico in ["beq", "bne"]:
        #Formato B para branch
        rs1 = int(partes_instruccion[1][1:])  # Quita la 'x' y convertir a entero
        rs2 = int(partes_instruccion[2][1:])  # Quita la 'x' y convertir a entero
        imm = int(partes_instruccion[3])  # Inmediato
        
        if mnemonico == "beq":
            opcode = 0b1100011
            funct3 = 0b000
        elif mnemonico == "bne":
            opcode = 0b1100011
            funct3 = 0b001
        
        imm = imm & 0xFFF  # Asegura que el inmediato sea de 12 bits
        
        # Ensamblar la instrucción en formato B
        imm_12 = (imm >> 12) & 0x1   # Bit 12 del inmediato
        imm_10_5 = (imm >> 5) & 0x3F # Bits 10-5 del inmediato
        imm_4_1 = (imm >> 1) & 0xF   # Bits 4-1 del inmediato
        imm_11 = (imm >> 11) & 0x1   # Bit 11 del inmediato
        
        word = (imm_12 << 31) | (imm_10_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_1 << 8) | (imm_11 << 7) | opcode
        return word

    raise NotImplementedError("encode_instruction: pendiente de implementar")


def explain_instruction(instruction: str, word: int) -> str:
    """
    Recibe la instrucción original (texto) y su codificación (word, 32 bits)
    ya calculada por encode_instruction, y retorna un texto explicativo
    que muestra los campos según el formato (R, I, S o B), con colores
    ANSI para diferenciar cada campo visualmente.
    """

    # ---------------- Colores ANSI ----------------
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    OPCODE  = "\033[91m"   # rojo
    RD      = "\033[92m"   # verde
    FUNCT3  = "\033[93m"   # amarillo
    RS1     = "\033[94m"   # azul
    RS2     = "\033[95m"   # magenta
    FUNCT7  = "\033[96m"   # cian
    IMM     = "\033[33m"   # naranja/dorado
    TITLE   = "\033[1;97m" # blanco brillante negrita
    DIM     = "\033[2m"    # atenuado (para bordes de tabla)

    def c(color, texto):
        return f"{color}{texto}{RESET}"

    def sign_extend(valor: int, bits: int) -> int:
        """Interpreta 'valor' como entero de 'bits' bits en complemento a 2."""
        signo = 1 << (bits - 1)
        return (valor & (signo - 1)) - (valor & signo)

    partes_instruccion = instruction.replace(",", " ").split()
    mnemonico = partes_instruccion[0]

    # Campos "crudos" comunes, extraídos por posición de bits del word de 32 bits.
    opcode = word & 0x7F
    rd     = (word >> 7)  & 0x1F
    funct3 = (word >> 12) & 0x7
    rs1    = (word >> 15) & 0x1F
    rs2    = (word >> 20) & 0x1F
    funct7 = (word >> 25) & 0x7F

    L = []
    L.append(c(TITLE, f"Instrucción analizada: {instruction}"))
    L.append(f"Codificación (32 bits): {BOLD}{word:032b}{RESET}")
    L.append("")

    borde = lambda s: c(DIM, s)

    # ---------------- Formato R: add, sub, and, or ----------------
    if mnemonico in ["add", "sub", "and", "or"]:
        L.append(c(TITLE, "Formato: R (registro-registro)"))
        L.append("")
        L.append(borde(" 31        25 24    20 19    15 14  12 11     7 6      0"))
        L.append(borde("+-----------+--------+--------+------+--------+-------+"))
        L.append(
            borde("| ") + c(FUNCT7, f"{funct7:07b}") + borde("   | ") +
            c(RS2, f"{rs2:05b}") + borde("  | ") +
            c(RS1, f"{rs1:05b}") + borde("  | ") +
            c(FUNCT3, f"{funct3:03b}") + borde("  | ") +
            c(RD, f"{rd:05b}") + borde("  |") +
            c(OPCODE, f"{opcode:07b}") + borde("|")
        )
        L.append(borde("+-----------+--------+--------+------+--------+-------+"))
        L.append(
            "  " + c(FUNCT7, "funct7") + "      " + c(RS2, "rs2") + "      " +
            c(RS1, "rs1") + "     " + c(FUNCT3, "funct3") + "   " +
            c(RD, "rd") + "     " + c(OPCODE, "opcode")
        )
        L.append("")
        L.append(c(TITLE, "Campos:"))
        L.append(f"  {c(OPCODE,'opcode')} [6:0]   = {c(OPCODE, f'{opcode:07b}')} -> identifica el formato R (operación registro-registro)")
        L.append(f"  {c(RD,'rd')}     [11:7]  = {c(RD, f'x{rd}')} ({c(RD, f'{rd:05b}')}) -> registro destino, recibe el resultado de '{mnemonico}'")
        L.append(f"  {c(FUNCT3,'funct3')} [14:12] = {c(FUNCT3, f'{funct3:03b}')} -> junto con funct7 selecciona la operación ({mnemonico})")
        L.append(f"  {c(RS1,'rs1')}    [19:15] = {c(RS1, f'x{rs1}')} ({c(RS1, f'{rs1:05b}')}) -> primer registro fuente (operando izquierdo)")
        L.append(f"  {c(RS2,'rs2')}    [24:20] = {c(RS2, f'x{rs2}')} ({c(RS2, f'{rs2:05b}')}) -> segundo registro fuente (operando derecho)")
        L.append(f"  {c(FUNCT7,'funct7')} [31:25] = {c(FUNCT7, f'{funct7:07b}')} -> distingue variantes con mismo opcode/funct3 (p.ej. add vs sub)")

    # ---------------- Formato I aritmético: addi, andi ----------------
    elif mnemonico in ["addi", "andi"]:
        imm_bits = (word >> 20) & 0xFFF
        imm = sign_extend(imm_bits, 12)
        L.append(c(TITLE, "Formato: I (aritmético con inmediato)"))
        L.append("")
        L.append(borde(" 31              20 19    15 14  12 11     7 6      0"))
        L.append(borde("+------------------+--------+------+--------+-------+"))
        L.append(
            borde("|   ") + c(IMM, f"{imm_bits:012b}") + borde("  | ") +
            c(RS1, f"{rs1:05b}") + borde("  | ") +
            c(FUNCT3, f"{funct3:03b}") + borde("  | ") +
            c(RD, f"{rd:05b}") + borde("  |") +
            c(OPCODE, f"{opcode:07b}") + borde("|")
        )
        L.append(borde("+------------------+--------+------+--------+-------+"))
        L.append(
            "      " + c(IMM, "imm[11:0]") + "        " + c(RS1, "rs1") +
            "    " + c(FUNCT3, "funct3") + "    " + c(RD, "rd") +
            "     " + c(OPCODE, "opcode")
        )
        L.append("")
        L.append(c(TITLE, "Campos:"))
        L.append(f"  {c(OPCODE,'opcode')} [6:0]   = {c(OPCODE, f'{opcode:07b}')} -> identifica el formato I aritmético")
        L.append(f"  {c(RD,'rd')}     [11:7]  = {c(RD, f'x{rd}')} ({c(RD, f'{rd:05b}')}) -> registro destino")
        L.append(f"  {c(FUNCT3,'funct3')} [14:12] = {c(FUNCT3, f'{funct3:03b}')} -> selecciona la operación ({mnemonico})")
        L.append(f"  {c(RS1,'rs1')}    [19:15] = {c(RS1, f'x{rs1}')} ({c(RS1, f'{rs1:05b}')}) -> registro fuente")
        L.append(f"  {c(IMM,'imm')}    [31:20] = {c(IMM, f'{imm_bits:012b}')} = {c(IMM, str(imm))} (decimal, con signo, 12 bits) -> operando inmediato")

    # ---------------- Formato I de carga: lw, lb ----------------
    elif mnemonico in ["lw", "lb"]:
        imm_bits = (word >> 20) & 0xFFF
        imm = sign_extend(imm_bits, 12)
        L.append(c(TITLE, "Formato: I (carga desde memoria)"))
        L.append("")
        L.append(borde(" 31              20 19    15 14  12 11     7 6      0"))
        L.append(borde("+------------------+--------+------+--------+-------+"))
        L.append(
            borde("|   ") + c(IMM, f"{imm_bits:012b}") + borde("  | ") +
            c(RS1, f"{rs1:05b}") + borde("  | ") +
            c(FUNCT3, f"{funct3:03b}") + borde("  | ") +
            c(RD, f"{rd:05b}") + borde("  |") +
            c(OPCODE, f"{opcode:07b}") + borde("|")
        )
        L.append(borde("+------------------+--------+------+--------+-------+"))
        L.append(
            "      " + c(IMM, "imm[11:0]") + "        " + c(RS1, "rs1") +
            "    " + c(FUNCT3, "funct3") + "    " + c(RD, "rd") +
            "     " + c(OPCODE, "opcode")
        )
        L.append("")
        L.append(c(TITLE, "Campos:"))
        L.append(f"  {c(OPCODE,'opcode')} [6:0]   = {c(OPCODE, f'{opcode:07b}')} -> identifica el formato I de carga")
        L.append(f"  {c(RD,'rd')}     [11:7]  = {c(RD, f'x{rd}')} ({c(RD, f'{rd:05b}')}) -> registro destino, recibe el valor leído de memoria")
        L.append(f"  {c(FUNCT3,'funct3')} [14:12] = {c(FUNCT3, f'{funct3:03b}')} -> indica el ancho del dato a cargar ({mnemonico})")
        L.append(f"  {c(RS1,'rs1')}    [19:15] = {c(RS1, f'x{rs1}')} ({c(RS1, f'{rs1:05b}')}) -> registro base (dirección)")
        L.append(f"  {c(IMM,'imm')}    [31:20] = {c(IMM, f'{imm_bits:012b}')} = {c(IMM, str(imm))} (decimal, con signo, 12 bits) -> desplazamiento (offset) respecto a rs1")

    # ---------------- Formato S: sw, sb ----------------
    elif mnemonico in ["sw", "sb"]:
        imm_11_5 = (word >> 25) & 0x7F
        imm_4_0  = (word >> 7)  & 0x1F
        imm_bits = (imm_11_5 << 5) | imm_4_0
        imm = sign_extend(imm_bits, 12)
        L.append(c(TITLE, "Formato: S (almacenamiento en memoria)"))
        L.append("")
        L.append(borde(" 31        25 24    20 19    15 14  12 11     7 6      0"))
        L.append(borde("+-----------+--------+--------+------+--------+-------+"))
        L.append(
            borde("| ") + c(IMM, f"{imm_11_5:07b}") + borde("   | ") +
            c(RS2, f"{rs2:05b}") + borde("  | ") +
            c(RS1, f"{rs1:05b}") + borde("  | ") +
            c(FUNCT3, f"{funct3:03b}") + borde("  |") +
            c(IMM, f"{imm_4_0:05b}") + borde("   |") +
            c(OPCODE, f"{opcode:07b}") + borde("|")
        )
        L.append(borde("+-----------+--------+--------+------+--------+-------+"))
        L.append(
            "  " + c(IMM, "imm[11:5]") + "    " + c(RS2, "rs2") + "      " +
            c(RS1, "rs1") + "    " + c(FUNCT3, "funct3") + "  " +
            c(IMM, "imm[4:0]") + "  " + c(OPCODE, "opcode")
        )
        L.append("")
        L.append(c(TITLE, "Campos:"))
        L.append(f"  {c(OPCODE,'opcode')}   [6:0]   = {c(OPCODE, f'{opcode:07b}')} -> identifica el formato S")
        L.append(f"  {c(IMM,'imm[4:0]')} [11:7]  = {c(IMM, f'{imm_4_0:05b}')} -> parte baja del inmediato (offset)")
        L.append(f"  {c(FUNCT3,'funct3')}   [14:12] = {c(FUNCT3, f'{funct3:03b}')} -> indica el ancho del dato a almacenar ({mnemonico})")
        L.append(f"  {c(RS1,'rs1')}      [19:15] = {c(RS1, f'x{rs1}')} ({c(RS1, f'{rs1:05b}')}) -> registro base (dirección)")
        L.append(f"  {c(RS2,'rs2')}      [24:20] = {c(RS2, f'x{rs2}')} ({c(RS2, f'{rs2:05b}')}) -> registro con el valor a almacenar")
        L.append(f"  {c(IMM,'imm[11:5]')}[31:25] = {c(IMM, f'{imm_11_5:07b}')} -> parte alta del inmediato")
        L.append(f"  Inmediato ensamblado = {{imm[11:5], imm[4:0]}} = {c(IMM, f'{imm_bits:012b}')} = {c(IMM, str(imm))} (decimal, con signo) -> offset respecto a rs1")

    # ---------------- Formato B: beq, bne ----------------
    elif mnemonico in ["beq", "bne"]:
        imm_12   = (word >> 31) & 0x1
        imm_10_5 = (word >> 25) & 0x3F
        imm_4_1  = (word >> 8)  & 0xF
        imm_11   = (word >> 7)  & 0x1
        imm_bits = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
        imm = sign_extend(imm_bits, 13)
        L.append(c(TITLE, "Formato: B (salto condicional)"))
        L.append("")
        L.append(borde(" 31 30      25 24    20 19    15 14  12 11    8  7  6      0"))
        L.append(borde("+---+---------+--------+--------+------+------+---+-------+"))
        L.append(
            borde("| ") + c(IMM, f"{imm_12}") + borde("|") + c(IMM, f"{imm_10_5:06b}") + borde("   | ") +
            c(RS2, f"{rs2:05b}") + borde("  | ") +
            c(RS1, f"{rs1:05b}") + borde("  | ") +
            c(FUNCT3, f"{funct3:03b}") + borde("  |") +
            c(IMM, f"{imm_4_1:04b}") + borde("  |") +
            c(IMM, f"{imm_11}") + borde("  |") +
            c(OPCODE, f"{opcode:07b}") + borde("|")
        )
        L.append(borde("+---+---------+--------+--------+------+------+---+-------+"))
        L.append(
            " " + c(IMM, "im[12]") + " " + c(IMM, "im[10:5]") + "  " + c(RS2, "rs2") +
            "      " + c(RS1, "rs1") + "   " + c(FUNCT3, "funct3") + " " +
            c(IMM, "im[4:1]") + " " + c(IMM, "im[11]") + " " + c(OPCODE, "opcode")
        )
        L.append("")
        L.append(c(TITLE, "Campos:"))
        L.append(f"  {c(OPCODE,'opcode')}    [6:0]   = {c(OPCODE, f'{opcode:07b}')} -> identifica el formato B")
        L.append(f"  {c(IMM,'imm[11]')}   [7]     = {c(IMM, str(imm_11))} -> bit 11 del inmediato")
        L.append(f"  {c(FUNCT3,'funct3')}    [14:12] = {c(FUNCT3, f'{funct3:03b}')} -> selecciona la condición de salto ({mnemonico})")
        L.append(f"  {c(RS1,'rs1')}       [19:15] = {c(RS1, f'x{rs1}')} ({c(RS1, f'{rs1:05b}')}) -> primer registro a comparar")
        L.append(f"  {c(RS2,'rs2')}       [24:20] = {c(RS2, f'x{rs2}')} ({c(RS2, f'{rs2:05b}')}) -> segundo registro a comparar")
        L.append(f"  {c(IMM,'imm[10:5]')} [30:25] = {c(IMM, f'{imm_10_5:06b}')} -> bits 10-5 del inmediato")
        L.append(f"  {c(IMM,'imm[12]')}   [31]    = {c(IMM, str(imm_12))} -> bit de signo del inmediato")
        L.append(f"  Inmediato ensamblado = {{imm[12],imm[11],imm[10:5],imm[4:1],1'b0}} = {c(IMM, str(imm))} (decimal, con signo)")
        L.append(f"  -> desplazamiento en bytes respecto al PC de la instrucción si '{mnemonico}' se cumple")

    

    return "\n".join(L)
    raise NotImplementedError("explain_instruction: pendiente de implementar")

def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
