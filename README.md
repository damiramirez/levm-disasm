# Disasm.py

Este script toma como input el `.txt` de los test fallados de EFTest. Obtiene los archivos `.json` que fallan, parsea el archivo para obtener la informacion necesaria y disasemblea el bytecode. El output es un archivo `.txt` con el bytecode disasembleado y nos indica si en los test que fallaron se usan `CALL`, `CREATE` o `CREATE2`.

```
GeneralStateTests/stRandom/randomStatetest85.json
CALL Transaction - to: 0x095e7baea6a6c7c4c2dfeb977efac326af552d87:
00000000: PUSH32 0xc350
00000021: PUSH32 0xc350
00000042: PUSH32 0x0
00000063: PUSH32 0x0
00000084: PUSH32 0x945304eb96065b2a98b57a48a06ae28d285a71b5
000000a5: PUSH32 0x1
000000c6: PUSH32 0x1
000000e7: PUSH32 0xc350
00000108: CALLCODE
00000109: JUMPDEST
0000010a: SSTORE
No CALL, CREATE, or CREATE2 found.
```

Por ahora solo se disasembla el bytecode del `to`. No tiene en cuenta al `calldata` ni en caso de que la transaccion sea de tipo `CREATE`.

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

   - **EFTEST-LEVM-DIR** es la ruta al directorio que contiene `levm_ef_tests_report.txt` y el subdirectorio `vectors` con los archivos JSON de los tests.
   - **OUTPUT-FILE**.txt es el archivo donde se almacenará el resultado.
