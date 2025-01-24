from http.client import HTTPException
from backend.etl.data_handler import DataHandler
from backend.api.models.liquefaction_zones import LiquefactionZone
from shapely.geometry import shape
from geoalchemy2.shape import from_shape


_LIQUEFACTION_URL = "https://gis.conservation.ca.gov/server/rest/services/CGS_Earthquake_Hazard_Zones/SHP_Liquefaction_Zones/MapServer/0/query"


class _LiquefactionDataHandler(DataHandler):
    """
    This class fetches, parses and loads SF liquefaction data from
    data.sfgov.org
    """

    def parse_data(self, data: dict) -> list[dict]:
        """
        Extracts feature attributes and geometry data to construct a
        list of dictionaries.

        Each dictionary represents a row for the database table.
        Geometry data is converted into a GeoAlchemy-compatible
        MultiPolygon with srid 4326.
        """
        features = data["features"]
        parsed_data = []
        for feature in features:
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            polygon = shape(geometry)  # Convert to shapely geometry (Polygon)
            transformed_multipolygon = self.transform_geometry(
                polygon, source_srid=3857, target_srid=4326
            )
            geoalchemy_multipolygon = from_shape(transformed_multipolygon, srid=4326)
            liquefaction_zone = {
                "identifier": properties.get("OBJECTID"),
                "geometry": geoalchemy_multipolygon,
                "shape_length": properties.get("Shape__Len", None),
                "shape_area": properties.get("Shape__Are", None),
            }
            parsed_data.append(liquefaction_zone)
        return parsed_data


if __name__ == "__main__":
    handler = _LiquefactionDataHandler(_LIQUEFACTION_URL, LiquefactionZone)
    try:
        params = {
            "where": "1=1",
            "geometry": "-13638270.49438025,4538285.617149651,-13620719.109495781,4555775.311559373",
            "geometryType": "esriGeometryEnvelope",
            "spatialRel": "esriSpatialRelIntersects",            
            "outFields": "*",
            "f": "geojson",
        }        

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Referer": "https://gis.conservation.ca.gov/",
        }        
        liquefaction_zones = handler.fetch_data(params, headers)
        liquefaction_zones_objects = handler.parse_data(liquefaction_zones)
        handler.bulk_insert_data(liquefaction_zones_objects, "identifier")
    except HTTPException as e:
        print(f"Failed after retries: {e}")
