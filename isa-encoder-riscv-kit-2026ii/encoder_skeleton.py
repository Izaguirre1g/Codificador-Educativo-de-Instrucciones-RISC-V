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
        #Instruccion tipo R
        rd = int(partes_instruccion[1][1:])  # Quita la 'x' y convertir a entero
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

        # Ensambla la instrucción en tipo R
        
        word = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return word
    #Instrucciones de formato I: addi, andi, lw, lb
    if mnemonico in ["addi", "andi"]:
        #Instruccion tipo I
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
        
        # Ensambla la instrucción en tipo I
        word = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return word

    #Instrucciones de formato I para load: lw, lb
    if mnemonico in ["lw", "lb"]:
        #Instruccion tipo I para load
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
        
        # Ensambla la instrucción en tipo I
        word = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return word           
    #Instrucciones de formato S: sw, sb
    if mnemonico in ["sw", "sb"]:
        #Instrucion tipo S para store
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
        
        # Ensambla la instrucción en tipo S
        imm_11_5 = (imm >> 5) & 0x7F #Inmediato de 7 bits (11-5) alto
        imm_4_0 = imm & 0x1F #Inmediato de 5 bits (4-0) bajo
        
        word = (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
        return word

    #Instrucciones de formato B: beq, bne
    if mnemonico in ["beq", "bne"]:
        #Instruccion tipo B para branch
        rs1 = int(partes_instruccion[1][1:])  # Quita la 'x' y convertir a entero
        rs2 = int(partes_instruccion[2][1:])  # Quita la 'x' y convertir a entero
        imm = int(partes_instruccion[3])  # Inmediato
        
        if mnemonico == "beq":
            opcode = 0b1100011
            funct3 = 0b000
        elif mnemonico == "bne":
            opcode = 0b1100011
            funct3 = 0b001
        
        imm = imm & 0x1FFF  # Asegura que el inmediato sea de 13 bits
        
        # Ensambla la instrucción en tipo B
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
    """
    Muestra la explicación de la codificación de una instrucción RISC-V.
    """

    partes = instruction.replace(",", " ").split()

    def signed_value(value, bits):
        if value & (1 << (bits - 1)):
            value -= (1 << bits)
        return value
    
    mnemonico = partes[0]

    salida = ""

    # Información general
    salida += f"Instrucción: {instruction}\n"
    salida += f"Hexadecimal: 0x{word:08x}\n"
    salida += f"Binario: {format(word, '032b')}\n\n"


    # ============================
    # Instruccion tipo R
    # ============================

    if mnemonico in ["add", "sub", "and", "or"]:

        salida += "Tipo de instruccion identificado: R\n\n"


        # Extraer campos desde la instrucción de 32 bits

        funct7 = (word >> 25) & 0x7F
        rs2 = (word >> 20) & 0x1F
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x07
        rd = (word >> 7) & 0x1F
        opcode = word & 0x7F


        # Representación visual

        salida += "Representación de campos:\n\n"

        salida += (
            "Bits:       31-25        24-20       19-15       "
            "14-12      11-7        6-0\n"
        )

        salida += (
            "Campo:      funct7       rs2         rs1         "
            "funct3     rd        opcode\n"
        )

        salida += (
            "            "
            f"{funct7:07b}      "
            f"{rs2:05b}       "
            f"{rs1:05b}         "
            f"{funct3:03b}     "
            f"{rd:05b}      "
            f"{opcode:07b}\n\n"
        )


        # Valores de los campos

        salida += "Valores de los campos:\n\n"

        salida += (
            f"funct7 : bits 31-25 = {funct7:07b} "
            f"({funct7})\n"
        )

        salida += (
            f"rs2    : bits 24-20 = {rs2:05b} "
            f"({rs2}) -> registro fuente x{rs2}\n"
        )

        salida += (
            f"rs1    : bits 19-15 = {rs1:05b} "
            f"({rs1}) -> registro fuente x{rs1}\n"
        )

        salida += (
            f"funct3 : bits 14-12 = {funct3:03b} "
            f"({funct3})\n"
        )

        salida += (
            f"rd     : bits 11-7  = {rd:05b} "
            f"({rd}) -> registro destino x{rd}\n"
        )

        salida += (
            f"opcode : bits 6-0   = {opcode:07b} "
            f"({opcode})\n"
        )


        # Explicación textual

        salida += "\nExplicación de los campos:\n\n"


        salida += (
            "funct7:\n"
            "Campo de 7 bits utilizado para identificar la operación "
            "específica dentro del formato R. "
            f"Para {mnemonico}, su valor es {funct7:07b}.\n\n"
        )


        salida += (
            "rs2:\n"
            "Registro fuente secundario. Contiene el segundo operando "
            f"de la operación. En esta instrucción corresponde a x{rs2}.\n\n"
        )


        salida += (
            "rs1:\n"
            "Registro fuente principal. Contiene el primer operando "
            f"de la operación. En esta instrucción corresponde a x{rs1}.\n\n"
        )


        salida += (
            "funct3:\n"
            "Campo de 3 bits que complementa a funct7 para determinar "
            f"la operación realizada. Para {mnemonico}, su valor es "
            f"{funct3:03b}.\n\n"
        )


        salida += (
            "rd:\n"
            "Registro destino donde se almacena el resultado de la "
            f"operación. En esta instrucción corresponde a x{rd}.\n\n"
        )


        salida += (
            "opcode:\n"
            "Campo de 7 bits que identifica el tipo de instrucción. "
            f"El valor {opcode:07b} indica que pertenece al conjunto "
            "de instrucciones tipo R.\n"
        )
        
        return salida

    # ============================
    # Instruccion tipo I
    # ============================
    elif mnemonico in ["addi", "andi", "lw", "lb"]:

        salida += "Formato identificado: I\n\n"


        imm = (word >> 20) & 0xFFF
        imm_signed = signed_value(imm, 12)
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x07
        rd = (word >> 7) & 0x1F
        opcode = word & 0x7F


        salida += "Representación de campos:\n\n"

        salida += (
            "Bits:       31-20        19-15      14-12      11-7       6-0\n"
        )

        salida += (
            "Campo:      imm          rs1        funct3     rd        opcode\n\n"
        )


        salida += (
            f"         {imm:012b}    "
            f"{rs1:05b}       "
            f"{funct3:03b}      "
            f"{rd:05b}      "
            f"{opcode:07b}\n\n"
        )


        salida += "Valores de los campos:\n\n"


        salida += (
            f"imm    : bits 31-20 = {imm:012b} "
            f"({imm_signed}) -> valor inmediato utilizado por la instrucción\n"
        )


        salida += (
            f"rs1    : bits 19-15 = {rs1:05b} "
            f"({rs1}) -> registro fuente x{rs1}\n"
        )


        salida += (
            f"funct3 : bits 14-12 = {funct3:03b} "
            f"({funct3}) -> identifica la operación específica\n"
        )


        salida += (
            f"rd     : bits 11-7 = {rd:05b} "
            f"({rd}) -> registro destino x{rd}\n"
        )


        salida += (
            f"opcode : bits 6-0 = {opcode:07b} "
            f"({opcode}) -> identifica el tipo de instrucción\n"
        )


        salida += "\nExplicación de los campos:\n\n"


        salida += (
            "imm:\n"
            "Campo inmediato de 12 bits. Contiene un valor constante "
            "utilizado por la operación o un desplazamiento de memoria "
            "en instrucciones load.\n\n"
        )


        salida += (
            "rs1:\n"
            "Registro fuente que contiene el primer operando o la dirección "
            "base en instrucciones de acceso a memoria.\n\n"
        )


        salida += (
            "funct3:\n"
            "Campo que diferencia las instrucciones dentro del mismo opcode. "
            "Por ejemplo, distingue addi de andi o lw de lb.\n\n"
        )


        salida += (
            "rd:\n"
            "Registro destino donde se almacena el resultado de la operación "
            "o el dato cargado desde memoria.\n\n"
        )


        salida += (
            "opcode:\n"
            "Identifica la categoría de la instrucción. "
            "Para este formato corresponde a instrucciones tipo I.\n"
        )
        return salida
    # ============================
    # Instruccion tipo S
    # ============================
    elif mnemonico in ["sw", "sb"]:

        salida += "Formato identificado: S\n\n"


        # Extraer campos del formato S

        imm_11_5 = (word >> 25) & 0x7F
        rs2 = (word >> 20) & 0x1F
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x07
        imm_4_0 = (word >> 7) & 0x1F
        opcode = word & 0x7F


        # Reconstrucción del inmediato

        imm = (imm_11_5 << 5) | imm_4_0

        imm_signed = signed_value(imm, 12)



        salida += "Representación de campos:\n\n"


        salida += (
            "Bits:       31-25        24-20       19-15       "
            "14-12      11-7        6-0\n"
        )

        salida += (
            "Campo:      imm[11:5]    rs2         rs1         "
            "funct3     imm[4:0]    opcode\n\n"
        )


        salida += (
            "            "
            f"{imm_11_5:07b}     "
            f"{rs2:05b}       "
            f"{rs1:05b}         "
            f"{funct3:03b}        "
            f"{imm_4_0:05b}      "
            f"{opcode:07b}\n\n"
        )



        salida += "Valores de los campos:\n\n"


        salida += (
            f"imm[11:5]: bits 31-25 = {imm_11_5:07b} "
            f"({imm_11_5}) -> parte superior del inmediato\n"
        )


        salida += (
            f"rs2      : bits 24-20 = {rs2:05b} "
            f"({rs2}) -> registro que contiene el dato a almacenar\n"
        )


        salida += (
            f"rs1      : bits 19-15 = {rs1:05b} "
            f"({rs1}) -> registro base de memoria x{rs1}\n"
        )


        salida += (
            f"funct3   : bits 14-12 = {funct3:03b} "
            f"({funct3}) -> identifica la operación específica\n"
        )


        salida += (
            f"imm[4:0] : bits 11-7  = {imm_4_0:05b} "
            f"({imm_4_0}) -> parte inferior del inmediato\n"
        )


        salida += (
            f"opcode   : bits 6-0   = {opcode:07b} "
            f"({opcode}) -> identifica instrucciones tipo S\n"
        )



        salida += "\nExplicación de los campos:\n\n"


        salida += (
            "imm[11:5] e imm[4:0]:\n"
            "El inmediato de las instrucciones tipo S está dividido en "
            "dos partes dentro de la instrucción. Ambas partes se unen "
            "para formar el desplazamiento de memoria de 12 bits.\n\n"
        )


        salida += (
            "rs2:\n"
            "Registro fuente que contiene el dato que será escrito en "
            "memoria.\n\n"
        )


        salida += (
            "rs1:\n"
            "Registro fuente que contiene la dirección base de memoria "
            "sobre la cual se aplicará el desplazamiento.\n\n"
        )


        salida += (
            "funct3:\n"
            "Campo que permite diferenciar las instrucciones de almacenamiento. "
            "Por ejemplo, distingue sw de sb.\n\n"
        )


        salida += (
            "opcode:\n"
            "Campo que identifica que la instrucción pertenece al formato S "
            "de acceso a memoria.\n"
        )

        return salida
    # ============================
    # Instruccion tipo B
    # ============================
    elif mnemonico in ["beq", "bne"]:

        salida += "Formato identificado: B\n\n"


        # Extraer campos del formato B

        imm_12 = (word >> 31) & 0x1
        imm_10_5 = (word >> 25) & 0x3F
        rs2 = (word >> 20) & 0x1F
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x07
        imm_4_1 = (word >> 8) & 0x0F
        imm_11 = (word >> 7) & 0x01
        opcode = word & 0x7F


        # Reconstruir inmediato completo

        imm = (
            (imm_12 << 12) |
            (imm_11 << 11) |
            (imm_10_5 << 5) |
            (imm_4_1 << 1)
        )

        imm_signed = signed_value(imm, 13)



        salida += "Representación de campos:\n\n"


        salida += (
            "Bits:        31      30-25       24-20       19-15       "
            "14-12      11-8       7        6-0\n"
        )

        salida += (
            "Campo:      imm12    imm10:5     rs2         rs1        "
            "funct3     imm4:1     imm11    opcode\n\n"
        )


        salida += (
            "             "
            f"{imm_12:b}       "
            f"{imm_10_5:06b}     "
            f"{rs2:05b}      "
            f"{rs1:05b}         "
            f"{funct3:03b}        "
            f"{imm_4_1:04b}        "
            f"{imm_11:b}      "
            f"{opcode:07b}\n\n"
        )



        salida += "Valores de los campos:\n\n"


        salida += (
            f"imm[12]   : bits 31     = {imm_12:b} "
            f"({imm_12})\n"
        )


        salida += (
            f"imm[10:5] : bits 30-25 = {imm_10_5:06b} "
            f"({imm_10_5})\n"
        )


        salida += (
            f"rs2       : bits 24-20 = {rs2:05b} "
            f"({rs2}) -> segundo registro comparado x{rs2}\n"
        )


        salida += (
            f"rs1       : bits 19-15 = {rs1:05b} "
            f"({rs1}) -> primer registro comparado x{rs1}\n"
        )


        salida += (
            f"funct3    : bits 14-12 = {funct3:03b} "
            f"({funct3})\n"
        )


        salida += (
            f"imm[4:1]  : bits 11-8  = {imm_4_1:04b} "
            f"({imm_4_1})\n"
        )


        salida += (
            f"imm[11]   : bit 7      = {imm_11:b} "
            f"({imm_11})\n"
        )


        salida += (
            f"opcode    : bits 6-0   = {opcode:07b} "
            f"({opcode})\n"
        )



        salida += "\nExplicación de los campos:\n\n"


        salida += (
            "imm[12], imm[11], imm[10:5], imm[4:1]:\n"
            "Estos campos forman el desplazamiento del salto. "
            "En las instrucciones tipo B el inmediato está dividido "
            "en varias posiciones dentro de la instrucción y debe "
            "reconstruirse para obtener el valor completo del branch.\n\n"
        )


        salida += (
            "rs1:\n"
            "Registro fuente que contiene el primer valor utilizado "
            "en la comparación.\n\n"
        )


        salida += (
            "rs2:\n"
            "Registro fuente que contiene el segundo valor utilizado "
            "en la comparación.\n\n"
        )


        salida += (
            "funct3:\n"
            "Define la condición del salto. "
            "Para beq corresponde a 000 y para bne corresponde a 001.\n\n"
        )


        salida += (
            "opcode:\n"
            "Identifica que la instrucción pertenece al formato B "
            "de instrucciones de salto condicional.\n"
        )
        return salida
    #raise NotImplementedError("explain_instruction: pendiente de implementar")


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
