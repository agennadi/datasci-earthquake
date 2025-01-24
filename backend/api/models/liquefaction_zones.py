"""All data of the Liquefaction Zones table from SFData"""

from sqlalchemy import Integer, String, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from geoalchemy2 import Geometry
from datetime import datetime
from backend.api.models.base import Base
from geoalchemy2.shape import to_shape
from shapely import to_geojson
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Index

class LiquefactionZone(Base):
    """
    All data of the Liquefaction Zones table from SFData

    Contains multipolygon geometries defining soil liquefaction zones
    as High (H) or Very High (VH) susceptibility
    """

    __tablename__ = "liquefaction_zones"

    identifier: Mapped[str] = mapped_column(
        String, primary_key=True
    )
    geometry: Mapped[Geometry] = mapped_column(Geometry("POLYGON", srid=4326), nullable=False)
    shape_length: Mapped[float] = mapped_column(Float, nullable=True)
    shape_area: Mapped[float] = mapped_column(Float, nullable=True)
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # Add a GIST index for the geometry column
    __table_args__ = (
        Index('idx_geometry', geometry, postgresql_using='gist'),
    )

    @hybrid_property
    def multipolygon_as_geosjon(self):
        """Convert multipolygons to a geojson"""
        return to_geojson(to_shape(self.geometry))

    def __repr__(self) -> str:
        return f"<LiquefactionZone(id={self.identifier})>"
