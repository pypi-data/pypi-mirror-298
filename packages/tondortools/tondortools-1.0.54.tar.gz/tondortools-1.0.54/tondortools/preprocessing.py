


from pydantic import BaseModel

import json
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, validator, root_validator, Field

from typing import List, Union, Optional

from dataclasses import dataclass, field
from typing import List, Dict
from pydantic import BaseModel, validator

@dataclass
class Tile:
    name: str
    epsg: int
    count: int

@dataclass
class Services:
    sub: List[str] = field(default_factory=list)
    dst: List[str] = field(default_factory=list)
    parcel_id: str = field(default_factory=str)
    FOI: List[str] = field(default_factory=list)
    split_overlap: bool = field(default_factory=bool)


def create_object(config_path):
    # Load the JSON from file or use your JSON string directly
    with open(config_path, 'r') as file:
        json_str = file.read()

    # Parse the JSON into the Configuration data class
    config = Configuration.parse_raw(json_str)
    return config


class Configuration(BaseModel):
    tiles: Optional[List[Tile]]= None
    services: Dict[str, Services]
    pixel: Dict[str, int] =  Field({})
    kult_conversion_table_name : Optional[str]= None
    conversion_table_original_column: Optional[str]= None
    conversion_table_target_column: Optional[str]= None
    classification_support_data: Optional[Path]= None
    gpkg_tile_column: Optional[str]= None
    min_parcel: int = Field(2000)
    subtile_count: int = Field(20)

    def get_service_info(self, service_name):
        for serivce_item_name, serive_attribute in self.services.items():
            if serivce_item_name == service_name:
                return serive_attribute

    def get_tile_info(self, tile_name):
        if self.tiles is not None:
            for tile_name_item in self.tiles:
                if tile_name_item.name == tile_name:
                    return tile_name_item
        else:
            return None