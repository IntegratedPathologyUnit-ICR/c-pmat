import xml.etree.ElementTree as ET
import json


def convert_aperio_xml_to_geojson(xml_path, output_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Create a GeoJSON FeatureCollection
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Extract microns per pixel from the root element
    microns_per_pixel = float(root.get('MicronsPerPixel', 1.0))

    # Find all Regions
    regions = root.findall(".//Region")

    for idx, region in enumerate(regions, 1):
        # Extract vertices
        vertices = region.find('Vertices')

        if vertices is not None:
            # Convert pixel coordinates to polygon coordinates
            polygon_coords = []
            for vertex in vertices.findall('Vertex'):
                x = float(vertex.get('X', 0))
                y = float(vertex.get('Y', 0))
                polygon_coords.append([x, y])

            # Close the polygon if not already closed
            if polygon_coords[0] != polygon_coords[-1]:
                polygon_coords.append(polygon_coords[0])

            # Determine the name for the annotation
            text = region.get('Text', '').strip()
            name = text if text else f'roi {idx}'

            # Create feature
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_coords]
                },
                "properties": {
                    "name": name,
                    "region_id": region.get('Id', ''),
                    "length": float(region.get('Length', 0)),
                    "area": float(region.get('Area', 0)),
                    "length_microns": float(region.get('LengthMicrons', 0)),
                    "area_microns": float(region.get('AreaMicrons', 0)),
                    "microns_per_pixel": microns_per_pixel
                }
            }

            geojson["features"].append(feature)

    # Write to GeoJSON file
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"Converted {len(geojson['features'])} regions to GeoJSON")


# Example usage
convert_aperio_xml_to_geojson(r'D:\Projects\cbias-nap-AMY\slides\1.xml', r'D:\Projects\cbias-nap-AMY\geojson\1.geojson')
print("Conversion complete. Check output.geojson")
