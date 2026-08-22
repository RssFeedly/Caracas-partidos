import urllib.request
import xml.etree.ElementTree as ET

# URL del canal de YouTube proporcionado
URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCQc3SSO8WacZt3L0IQe08Pg"

def filter_feed():
    # Descargar el feed original
    req = urllib.request.urlopen(URL)
    xml_data = req.read()

    # Parsear el XML (YouTube usa el espacio de nombres Atom)
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    # Recorrer las entradas (videos) y eliminar las que no cumplan la condición
    for entry in root.findall("atom:entry", ns):
        title_el = entry.find("atom:title", ns)
        if title_el is not None and title_el.text:
            title = title_el.text.lower()
            # Ambas palabras deben estar en el título
            if "resumen" not in title or "caracas" not in title:
                root.remove(entry)
        else:
            root.remove(entry)

    # Guardar el resultado filtrado en un nuevo archivo XML
    tree = ET.ElementTree(root)
    tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    filter_feed()
