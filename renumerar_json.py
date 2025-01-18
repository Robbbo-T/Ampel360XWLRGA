import json
import os
import shutil
import csv

def crear_backup(nombre_archivo):
    """
    Crea una copia de seguridad del archivo JSON original.
    """
    backup_archivo = f"{nombre_archivo}.backup.json"
    shutil.copy(nombre_archivo, backup_archivo)
    print(f"Copia de seguridad creada: {backup_archivo}")

def validar_renumeracion(renumeracion_ids, renumeracion_numeros):
    """
    Verifica que no haya IDs o números de capítulos duplicados en los mapeos de renumeración.
    """
    # Verificar IDs
    if len(set(renumeracion_ids.values())) != len(renumeracion_ids):
        raise ValueError("La renumeración de IDs contiene IDs de capítulo duplicados.")
    
    # Verificar números de capítulos
    if len(set(renumeracion_numeros.values())) != len(renumeracion_numeros):
        raise ValueError("La renumeración de números de capítulos contiene números duplicados.")

def extraer_ids(data):
    """
    Extrae todos los IDs actuales del documento para evitar duplicados.
    """
    ids = set()

    def recorrer(seccion):
        for clave, contenido in seccion.items():
            if clave == "Cross-Reference":
                continue
            if isinstance(contenido, list):
                for capitulo in contenido:
                    if isinstance(capitulo, dict) and "id" in capitulo:
                        ids.add(capitulo["id"])
            elif isinstance(contenido, dict):
                recorrer(contenido)

    for division in data.get("One Legend G&A", {}).values():
        recorrer(division)

    return ids

def renumerar_capitulos_y_referencias(data, renumeracion_ids, renumeracion_numeros):
    """
    Renumera los capítulos y actualiza las referencias cruzadas en todo el documento JSON.
    Utiliza funciones recursivas para manejar múltiples niveles de secciones y sub-secciones.
    """
    capitulos_renumerados = set()
    ids_existentes = extraer_ids(data)

    def procesar_seccion(seccion):
        for clave, contenido in seccion.items():
            if clave == "Cross-Reference":
                # Actualizar referencias cruzadas
                nueva_cross_ref = {}
                for old_id, referencias in contenido.items():
                    nuevo_id = renumeracion_ids.get(old_id, old_id)
                    
                    # Validar que todas las referencias existan en el mapeo o en los IDs existentes
                    for ref in referencias:
                        if ref not in renumeracion_ids and ref not in ids_existentes:
                            raise ValueError(f"Referencia cruzada inválida: {ref} no está en el mapeo de renumeración ni existe en el documento.")
                    
                    # Renumerar las referencias
                    nueva_referencias = [renumeracion_ids.get(ref, ref) for ref in referencias]
                    nueva_cross_ref[nuevo_id] = nueva_referencias
                # Actualizar la sección de Cross-Reference con las nuevas referencias
                seccion["Cross-Reference"] = nueva_cross_ref
            elif isinstance(contenido, list):
                for capitulo in contenido:
                    if isinstance(capitulo, dict) and "id" in capitulo and "Chapter" in capitulo:
                        old_id = capitulo["id"]
                        old_num = capitulo["Chapter"]
                        if old_id in renumeracion_ids:
                            nuevo_id = renumeracion_ids[old_id]
                            nuevo_num = renumeracion_numeros.get(old_num, old_num)
                            
                            # Validar que el nuevo_id no esté ya asignado
                            if nuevo_id in capitulos_renumerados:
                                raise ValueError(f"Duplicado detectado: ID de capítulo {nuevo_id} ya ha sido asignado.")
                            
                            capitulo["id"] = nuevo_id
                            capitulo["Chapter"] = nuevo_num
                            capitulos_renumerados.add(nuevo_id)
            elif isinstance(contenido, dict):
                # Llamada recursiva para sub-secciones
                procesar_seccion(contenido)

    for division in data.get("One Legend G&A", {}).values():
        for seccion_key, seccion in division.items():
            procesar_seccion(seccion)

    return data

def exportar_json_a_csv(data, output_dir='csv_exports'):
    """
    Exporta cada sección del JSON a un archivo CSV.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for division_key, division in data.get("One Legend G&A", {}).items():
        for seccion_key, seccion in division.items():
            # Crear un archivo CSV para cada sección
            nombre_archivo = f"{seccion_key}.csv"
            ruta_archivo = os.path.join(output_dir, nombre_archivo)
            
            # Obtener los capítulos y las referencias cruzadas
            capitulos = []
            cross_references = seccion.get("Cross-Reference", {})
            
            # Iterar sobre todas las listas de capítulos dentro de la sección
            for sub_seccion_key, sub_seccion_contenido in seccion.items():
                if isinstance(sub_seccion_contenido, list):
                    for capitulo in sub_seccion_contenido:
                        if isinstance(capitulo, dict) and "id" in capitulo and "Chapter" in capitulo:
                            capitulo_num = capitulo.get("Chapter", "")
                            id_capitulo = capitulo.get("id", "")
                            titulo = capitulo.get("Title", "")
                            ata = ", ".join(capitulo.get("ATA iSpec 2200", []))
                            referencias = ", ".join(cross_references.get(id_capitulo, []))
                            capitulos.append({
                                'Capítulo': capitulo_num,
                                'ID': id_capitulo,
                                'Título': titulo,
                                'ATA iSpec 2200': ata,
                                'Referencias Cruzadas': referencias
                            })
            
            # Escribir a CSV solo si hay capítulos
            if capitulos:
                with open(ruta_archivo, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Capítulo', 'ID', 'Título', 'ATA iSpec 2200', 'Referencias Cruzadas']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for capitulo in capitulos:
                        writer.writerow(capitulo)
                
                print(f"Exportado: {ruta_archivo}")
            else:
                print(f"No se encontraron capítulos para exportar en la sección: {seccion_key}")

def main():
    nombre_archivo = 'documento.json'
    archivo_backup = f"{nombre_archivo}.backup.json"
    archivo_actualizado = 'documento_actualizado.json'

    try:
        # Verificar si el archivo JSON existe
        if not os.path.exists(nombre_archivo):
            raise FileNotFoundError(f"El archivo '{nombre_archivo}' no se encontró.")

        # Crear una copia de seguridad antes de modificar
        crear_backup(nombre_archivo)

        # Cargar el documento JSON original
        with open(nombre_archivo, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Definir los mapeos de renumeración
        renumeracion_ids = {
            "CH1": "CH2",
            "CH2": "CH1",
            "CH3": "CH4",
            "CH4": "CH3",
            "CH5": "CH6",
            "CH6": "CH5",
            "CH7": "CH8",
            "CH8": "CH7",
            "CH9": "CH10",
            "CH10": "CH9",
            "CH11": "CH12",
            "CH12": "CH11",
            "CH13": "CH14",
            "CH14": "CH13",
            "CH15": "CH16",
            "CH16": "CH15",
            "CH17": "CH18",
            "CH18": "CH17",
            "CH19": "CH20",
            "CH20": "CH19",
            "CH21": "CH22",
            "CH22": "CH21",
            "CH23": "CH24",
            "CH24": "CH23",
            "CH25": "CH26",
            "CH26": "CH25",
            "CH27": "CH28",
            "CH28": "CH27",
            "CH29": "CH30",
            "CH30": "CH29",
            "CH31": "CH32",
            "CH32": "CH31",
            "CH33": "CH34",
            "CH34": "CH33",
            "CH35": "CH36",
            "CH36": "CH35",
            "CH37": "CH38",
            "CH38": "CH37",
            "CH39": "CH40",
            "CH40": "CH39",
            "CH41": "CH42",
            "CH42": "CH41",
            "CH43": "CH44",
            "CH44": "CH43",
            "CH45": "CH46",
            "CH46": "CH45",
            "CH47": "CH48",
            "CH48": "CH47",
            "CH49": "CH50",
            "CH50": "CH49",
            "CH51": "CH52",
            "CH52": "CH51",
            "CH53": "CH54",
            "CH54": "CH53",
            "CH55": "CH56",
            "CH56": "CH55",
            "CH57": "CH58",
            "CH58": "CH57",
            "CH59": "CH60",
            "CH60": "CH59",
            "CH61": "CH62",
            "CH62": "CH61",
            "CH63": "CH64",
            "CH64": "CH63",
            "CH65": "CH66",
            "CH66": "CH65",
            "CH67": "CH68",
            "CH68": "CH67",
            "CH69": "CH70",
            "CH70": "CH69",
            "CH71": "CH72",
            "CH72": "CH71",
            "CH73": "CH74",
            "CH74": "CH73",
            "CH75": "CH76",
            "CH76": "CH75",
            "CH77": "CH78",
            "CH78": "CH77",
            "CH79": "CH80",
            "CH80": "CH79",
            "CH81": "CH82",
            "CH82": "CH81",
            "CH83": "CH84",
            "CH84": "CH83",
            "CH85": "CH86",
            "CH86": "CH85",
            "CH87": "CH88",
            "CH88": "CH87",
            "CH89": "CH90",
            "CH90": "CH89",
            "CH91": "CH92",
            "CH92": "CH91",
            "CH93": "CH94",
            "CH94": "CH93",
            "CH95": "CH96",
            "CH96": "CH95",
            "CH97": "CH98",
            "CH98": "CH97",
            "CH99": "CH99"  # Asumiendo que el capítulo 99 no cambia
        }

        renumeracion_numeros = {
            1: 2,
            2: 1,
            3: 4,
            4: 3,
            5: 6,
            6: 5,
            7: 8,
            8: 7,
            9: 10,
            10: 9,
            11: 12,
            12: 11,
            13: 14,
            14: 13,
            15: 16,
            16: 15,
            17: 18,
            18: 17,
            19: 20,
            20: 19,
            21: 22,
            22: 21,
            23: 24,
            24: 23,
            25: 26,
            26: 25,
            27: 28,
            28: 27,
            29: 30,
            30: 29,
            31: 32,
            32: 31,
            33: 34,
            34: 33,
            35: 36,
            36: 35,
            37: 38,
            38: 37,
            39: 40,
            40: 39,
            41: 42,
            42: 41,
            43: 44,
            44: 43,
            45: 46,
            46: 45,
            47: 48,
            48: 47,
            49: 50,
            50: 49,
            51: 52,
            52: 51,
            53: 54,
            54: 53,
            55: 56,
            56: 55,
            57: 58,
            58: 57,
            59: 60,
            60: 59,
            61: 62,
            62: 61,
            63: 64,
            64: 63,
            65: 66,
            66: 65,
            67: 68,
            68: 67,
            69: 70,
            70: 69,
            71: 72,
            72: 71,
            73: 74,
            74: 73,
            75: 76,
            76: 75,
            77: 78,
            78: 77,
            79: 80,
            80: 79,
            81: 82,
            82: 81,
            83: 84,
            84: 83,
            85: 86,
            86: 85,
            87: 88,
            88: 87,
            89: 90,
            90: 89,
            91: 92,
            92: 91,
            93: 94,
            94: 93,
            95: 96,
            96: 95,
            97: 98,
            98: 97,
            99: 99  # Asumiendo que el capítulo 99 no cambia
        }

        # Validar el mapeo de renumeración
        validar_renumeracion(renumeracion_ids, renumeracion_numeros)

        # Renumerar capítulos y actualizar referencias cruzadas
        data_actualizada = renumerar_capitulos_y_referencias(data, renumeracion_ids, renumeracion_numeros)

        # Exportar el JSON actualizado a CSV
        exportar_json_a_csv(data_actualizada)

        # Guardar el documento JSON actualizado
        with open(archivo_actualizado, 'w', encoding='utf-8') as file:
            json.dump(data_actualizada, file, ensure_ascii=False, indent=2)

        print(f"Renumeración, actualización de referencias y exportación a CSV completadas exitosamente. Archivo actualizado: {archivo_actualizado}")

if __name__ == "__main__":
    main()

