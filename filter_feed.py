import urllib.request
import xml.etree.ElementTree as ET
from xml.dom import minidom

URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCQc3SSO8WacZt3L0IQe08Pg"

def filter_feed():
    req = urllib.request.urlopen(URL)
    xml_data = req.read()

    # Parsear Atom original de YouTube
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}

    # Crear la estructura de un RSS 2.0 limpio
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    title_channel = root.find("atom:title", ns)
    ET.SubElement(channel, "title").text = title_channel.text if title_channel is not None else "YouTube Filtered Feed"
    ET.SubElement(channel, "link").text = URL
    ET.SubElement(channel, "description").text = "Feed filtrado de YouTube con palabras clave"

    # Filtrar y agregar solo los videos que contengan ambas palabras
    for entry in root.findall("atom:entry", ns):
        title_el = entry.find("atom:title", ns)
        if title_el is not None and title_el.text:
            title_text = title_el.text
            title_lower = title_text.lower()
            
            # Condición: Ambas palabras deben estar en el título
            if "resumen" in title_lower and "caracas" in title_lower:
                item = ET.SubElement(channel, "item")
                ET.SubElement(item, "title").text = title_text
                
                # Obtener link del video
                link_el = entry.find("atom:link", ns)
                if link_el is not None and "href" in link_el.attrib:
                    ET.SubElement(item, "link").text = link_el.attrib["href"]
                
                # ID único y fecha
                id_el = entry.find("atom:id", ns)
                if id_el is not None:
                    ET.SubElement(item, "guid").text = id_el.text
                
                published_el = entry.find("atom:published", ns)
                if published_el is not None:
                    ET.SubElement(item, "pubDate").text = published_el.text

    # Guardar como XML formateado
    rough_string = ET.tostring(rss, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="2")

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    filter_feed()
