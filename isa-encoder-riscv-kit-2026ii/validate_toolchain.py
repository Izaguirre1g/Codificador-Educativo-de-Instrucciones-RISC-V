import subprocess
import tempfile
import re
import csv

from encoder_skeleton import encode_instruction


PRUEBAS = [

    # ======================
    # FORMATO R
    # ======================

    "add x5, x6, x7",
    "add x28, x15, x0",
    "add x31, x30, x29",

    "sub x5, x6, x7",
    "sub x10, x10, x0",
    "sub x31, x30, x29",

    "and x5, x6, x7",
    "and x10, x10, x0",
    "and x31, x30, x29",

    "or x5, x6, x7",
    "or x10, x10, x0",
    "or x31, x30, x29",


    # ======================
    # FORMATO I
    # ======================

    "addi x5, x6, 10",
    "addi x10, x1, -12",
    "addi x31, x30, 2047",

    "andi x5, x6, 10",
    "andi x10, x1, -12",
    "andi x31, x30, 2047",


    # ======================
    # LOAD
    # ======================

    "lw x5, 8(x6)",
    "lw x10, -16(x1)",
    "lw x31, 2047(x30)",

    "lb x5, 8(x6)",
    "lb x10, -16(x1)",
    "lb x31, 2047(x30)",


    # ======================
    # FORMATO S
    # ======================

    "sw x5, 8(x6)",
    "sw x10, -16(x1)",
    "sw x31, 2047(x30)",

    "sb x5, 8(x6)",
    "sb x10, -16(x1)",
    "sb x31, 2047(x30)",


    # ======================
    # FORMATO B
    # ======================

    "beq x5, x6, 8",
    "beq x10, x1, -4",
    "beq x31, x30, 1024",

    "bne x5, x6, 8",
    "bne x10, x1, -4",
    "bne x31, x30, 1024",
]


def objdump_hex(instruction):

    if instruction.startswith("beq") or instruction.startswith("bne"):

        partes = instruction.replace(",", "").split()

        mnemonico = partes[0]
        rs1 = partes[1]
        rs2 = partes[2]
        offset = int(partes[3])


        # Salto hacia adelante
        if offset > 0:

            cantidad_nops = (offset // 4) - 1

            asm = f"""
.text

.globl main

main:

    {mnemonico} {rs1}, {rs2}, label
"""

            for _ in range(cantidad_nops):
                asm += "\n    nop"

            asm += """

label:
    nop
"""


        # Salto hacia atrás
        else:

            cantidad_nops = abs(offset) // 4

            asm = """
.text

.globl main

label:
"""

            for _ in range(cantidad_nops):
                asm += "\n    nop"

            asm += f"""

main:

    {mnemonico} {rs1}, {rs2}, label
"""


    else:

        asm = f"""
.text

.globl main

main:

    {instruction}
"""


    with tempfile.NamedTemporaryFile(
        suffix=".s",
        mode="w",
        delete=False
    ) as archivo:

        archivo.write(asm)
        nombre_s = archivo.name


    nombre_o = nombre_s.replace(".s", ".o")


    subprocess.run(
        [
            "riscv64-unknown-elf-as",
            "-march=rv32i",
            "-mabi=ilp32",
            "-o",
            nombre_o,
            nombre_s
        ],
        check=True,
        capture_output=True
    )


    resultado = subprocess.run(
        [
            "riscv64-unknown-elf-objdump",
            "-d",
            nombre_o
        ],
        capture_output=True,
        text=True
    )


    salida = resultado.stdout


    matches = re.findall(
        r"\s[0-9a-f]+:\s+([0-9a-f]{8})",
        salida
    )


    if matches:

        # Para branches negativos el branch aparece después del nop
        if instruction.startswith("beq") or instruction.startswith("bne"):

            if "-" in instruction:
                return matches[-1]

            return matches[0]


        return matches[0]


    return "ERROR"



def main():

    resultados = []


    for instruccion in PRUEBAS:

        modelo = encode_instruction(instruccion)

        modelo_hex = f"{modelo:08x}"


        oficial = objdump_hex(instruccion)


        coincide = modelo_hex == oficial


        resultados.append(
            [
                instruccion,
                "0x" + modelo_hex,
                "0x" + oficial,
                coincide
            ]
        )


        print(
            instruccion,
            modelo_hex,
            oficial,
            "OK" if coincide else "ERROR"
        )


    with open(
        "validacion_toolchain.csv",
        "w",
        newline=""
    ) as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow(
            [
                "Instruccion",
                "Modelo",
                "objdump",
                "Coincide"
            ]
        )

        escritor.writerows(resultados)



    print("\nArchivo generado: validacion_toolchain.csv")



if __name__ == "__main__":
    main()