class FileReader:
    """
    Clase para leer archivos de texto línea por línea o acceder a líneas específicas.
    """

    def __init__(self, file_path, encoding="utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def read_all_lines(self):
        """
        Generador que devuelve cada línea del archivo.
        """
        with open(self.file_path, "r", encoding=self.encoding) as f:
            for linea in f:
                yield linea.strip()

    def read_line(self, line_number):
        """
        Devuelve la línea específica según el número proporcionado (empezando en 0).
        Si no existe, devuelve None.
        """
        with open(self.file_path, "r", encoding=self.encoding) as f:
            for i, linea in enumerate(f, start=0):
                if i == line_number:
                    return linea.strip()
        return None
