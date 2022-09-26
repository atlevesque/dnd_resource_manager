from dataclasses import dataclass

from dndresmanager.constants import RestTypes



@dataclass
class Resource():
    rank: int
    resource_name: str
    max_uses : int
    uses_left: int
    rest_type: RestTypes

    # def __init__(self, *args, **kwargs):
    #     # super().__init__(*args, **kwargs)
    #     self.rest_type = REST_TYPE_MAPPINGS[self.encoded_rest_type]


