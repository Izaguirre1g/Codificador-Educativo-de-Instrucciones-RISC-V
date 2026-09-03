## 1. Instalación del toolchain RISC-V

El proyecto fue validado utilizando el siguiente toolchain:

Instalación en Ubuntu:

```bash
sudo apt update

sudo apt install binutils-riscv64-unknown-elf
riscv64-unknown-elf-as --version
riscv64-unknown-elf-objdump --version
``` 
## 2. Uso de la herramienta 

Se debe ingresar a la linea de comandos del sistema, en este caso se utilizo Ubuntu.
Una vez en el CLI se deben colocar los siguientes comandos: 
```
printf 'add x5, x6, x7\n' > /tmp/t.s
riscv64-unknown-elf-as -march=rv32i -mabi=ilp32 -o /tmp/t.o /tmp/t.s
riscv64-unknown-elf-objdump -d /tmp/t.o
```
Con esto se podra ver el valor que genera el toolchain y luego comparar el valor con lo que se hizo a mano.
## 3. Uso del ./run.sh
En caso de que el comando no funcione se debe colocar primero el siguiente comando:
```
chmod +x run.sh
```
Finalmente se puede ejecutar el siguiente comando con su correspondiente instruccion:
```
./run.sh "instruccion"
```
Luego de eso se mostrara la informacion correspondiente con la instruccion ingresada

## 4. Correr los 36 casos de prueba
Para correr los 36 casos de prueba se debe estar en el CLI y correr el siguiente comando:
```
python3 test_toolchain.py
```
Ya que por medio de ese .py se toman las instrucciones y se hace el tratamiento de pasarlas a hex y luego hacer la comparacion con el resultado del toolchain; de caso extra se crea un archivo .cvs para tener la informacion. En la siguiente se muestra el resultado esperado:
![alt text](/images/image.png)
## 5. Instalacion de Python
Para tener Python se deben tener los siguientes comandos:
```
sudo apt update
sudo apt install python3
python3 --version
sudo apt install python3-pip
sudo apt install python3-venv python3-dev
```

Requisitos:

- Python 3
- Ubuntu/Linux
- Toolchain RISC-V instalado
