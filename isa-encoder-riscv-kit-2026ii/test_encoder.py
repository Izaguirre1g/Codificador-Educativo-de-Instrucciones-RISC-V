from encoder_skeleton import encode_instruction

instruccion = "add x7, x20, x6"

resultado = encode_instruction(instruccion)

print("Decimal:", resultado)

print(f"Hex: 0x{resultado:08x}")

print("Binario:", format(resultado, "032b"))
