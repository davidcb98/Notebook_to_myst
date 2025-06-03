import re

def reemplazo_includegraphics(line):
    patron_includegraphics = r"\\includegraphics\s*\[width\s*=\s*(\d+(\.\d+)?)\s*\\linewidth\s*\]\s*\{([^}]+)\}"

    # Definir la función de reemplazo
    def reemplazo_includegraphics_aux(match):
        width = float(match.group(1))
        nombre_archivo = match.group(3)
        nueva_width = int(width * 1000)
        return f"<img src=\"{nombre_archivo}\" alt=\"\" align=center width='{nueva_width}px'/>"

    # Realizar el reemplazo
    return re.sub(patron_includegraphics, reemplazo_includegraphics_aux, line)

# Ejemplo de uso
linea = r"\includegraphics[width=0.7\linewidth]{Figuras/Fig_medidas2_nbasis_measure2}"
nueva_linea = reemplazo_includegraphics(linea)
print(nueva_linea)
