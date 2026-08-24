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
