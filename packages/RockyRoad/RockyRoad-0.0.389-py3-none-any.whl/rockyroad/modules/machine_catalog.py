from .module_imports import key
from uplink import (
    Consumer,
    post,
    patch,
    delete,
    returns,
    headers,
    Body,
    json,
    Query,
)
from uplink import get as http_get


@headers({"Ocp-Apim-Subscription-Key": key})
class Catalog(Consumer):
    """Inteface to Machine Catalog resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("machines/catalog")
    def list(self, machine_catalog_uid: Query = None, brand: Query = None, fuzzy_search_term: Query = None, fuzzy_match_limit: Query = None, fuzzy_scorer: Query = None):
        """This call will return detailed machine catalog information for the id specified or all machine catalog information if uid is specified."""

    @returns.json
    @json
    @post("machines/catalog")
    def insert(self, new_machine_catalog: Body):
        """This call will create a Machine Catalog entry with the specified parameters."""

    @delete("machines/catalog/{uid}")
    def delete(self, uid: str):
        """This call will delete the Machine Catalog entry for the specified Machine Catalog uid."""

    @json
    @patch("machines/catalog/{uid}")
    def update(self, uid: str, machine_catalog: Body):
        """This call will update the Machine Catalog with the specified parameters."""
