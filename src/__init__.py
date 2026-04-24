import sys
import os

# Agregar el directorio raíz al path cuando se importe este paquete
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)
