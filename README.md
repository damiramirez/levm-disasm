# Disasm.py

Este script toma como input el `.txt` de los test fallados de EFTest. Obtiene los archivos .json que fallan, parsea el archivo para obtener la informacion necesaria y disasemblea el bytecode. El output es un archivo `.txt` con el bytecode disasembleado y nos indica si en los test que fallaron se usan `CALL`, `CREATE` o `CREATE2`

## Requisitos

- Python 3.x
- `evmasm` (debe estar [instalado](https://github.com/crytic/pyevmasm?tab=readme-ov-file#installation) y disponible en el PATH)

## Uso

1. Antes de ejecutar este script, tenemos que chequear que exista el `levm_ef_tests_report.txt` ya que lo usa como entrada.
2. Ejecuta el script:

   ```sh
   python disasm.py --path <EFTEST-LEVM-DIR> > <OUTPUT-FILE>.txt
   ```

   Donde:

   - <EFTEST-LEVM-DIR> es la ruta al directorio que contiene `levm_ef_tests_report.txt` y el subdirectorio `vectors` con los archivos JSON de los tests.
   - <OUTPUT-FILE>.txt es el archivo donde se almacenará el resultado.
