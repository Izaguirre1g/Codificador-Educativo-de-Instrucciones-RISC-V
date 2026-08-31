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
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
    # TODO: implementar.
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
