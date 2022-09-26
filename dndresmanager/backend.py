import json

from dndresmanager.resource import Resource
from dndresmanager.constants import RestTypes, REST_TYPE_MAPPINGS



class Backend():
    character_name = ""
    character_resources:dict[int,Resource] = {}

    def __init__(self, filepath:str):
        with open(filepath,"r") as f:
            character_content = json.load(f)
        self.character_name = character_content.get("name","N/A")
        for rank, resource in enumerate(character_content.get("resources",[])):
            rest_type = resource.pop("rest_type")
            self.character_resources[rank] = Resource(
                        rank=rank,
                        **resource,
                        rest_type = REST_TYPE_MAPPINGS[rest_type]
                    )

    def decrement_resource(self, resource_rank:int)->int:
        resource = self.character_resources[resource_rank]
        resource.uses_left = max(resource.uses_left-1 , 0)
        return resource.uses_left, resource.max_uses

    def increment_resource(self, resource_rank:int)->int:
        resource = self.character_resources[resource_rank]
        resource.uses_left = min(resource.uses_left + 1 , resource.max_uses)
        return resource.uses_left, resource.max_uses

    def take_rest(self, rest_type:RestTypes):
        print(f"Taking {rest_type} rest")
        for _, resource in self.character_resources.items():
            if resource.rest_type == rest_type:
                resource.uses_left = resource.max_uses
        if rest_type == RestTypes.LONG:
            self.take_rest(RestTypes.SHORT)


if __name__ == "__main__":
    be = Backend("Sopafine.json")
    try:
        print("Decrementing first resource")
        be.decrement_resource(0)
        assert(be.character_resources[0].uses_left==0)
        be.decrement_resource(0)
        assert(be.character_resources[0].uses_left==0)
        be.increment_resource(1)
        assert(be.character_resources[1].uses_left==1)
        be.decrement_resource(1)
        assert(be.character_resources[1].uses_left==0)
        be.take_rest(RestTypes.SHORT)
        assert(be.character_resources[0].uses_left==1)
        assert(be.character_resources[1].uses_left==1)

        
        be.decrement_resource(0)
        be.decrement_resource(1)
        be.decrement_resource(2)
        
        assert(be.character_resources[0].uses_left==0)
        assert(be.character_resources[1].uses_left==0)
        assert(be.character_resources[2].uses_left==2)
        be.take_rest(RestTypes.LONG)
        assert(be.character_resources[0].uses_left==1)
        assert(be.character_resources[1].uses_left==1)
        assert(be.character_resources[2].uses_left==3)

    except Exception as e:
        print(be.character_resources)
        raise e

    
