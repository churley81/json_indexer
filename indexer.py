import json

class Indexed:
    def __init__(self, json_string):
        indexed = index_object(json_string)
        self.property_names = indexed['property_names']
        self.property_parents = indexed['property_parents']
        self.property_types = indexed['property_types']
        self.container_references = indexed['container_references']

class InvalidJSONForIndexingError(Exception):
      pass

def index_object(json_string):

    data = json.loads(json_string)
    if not isinstance(data, dict):
        raise InvalidJSONForIndexingError

    container_types = (tuple, list, dict)
    container_reference_list = []
    property_parent_list = []
    property_name_list = []
    property_type_list = []
    container_to_property_map = {}

    container_index = 0
    future_container_index = 1
    property_index = 1

    container_reference_list.append(data)
    property_parent_list.append(-1)
    property_name_list.append('')
    property_type_list.append(type(data))
    container_to_property_map[0] = 0

    while container_index < future_container_index:
        container = container_reference_list[container_index]
        if not isinstance(container, list):
            base_keys = container.keys()
            for key in base_keys:
                property_parent_list.append(container_to_property_map[container_index])
                property_name_list.append(key)
                property_type_list.append(type(container[key]))
                if isinstance(container[key], container_types):
                    container_reference_list.append(container[key])
                    container_to_property_map[future_container_index] = property_index
                    future_container_index += 1
                property_index += 1
        else:
            element_index = 0
            for element in container:
                property_parent_list.append(container_to_property_map[container_index])
                property_name_list.append(element_index)
                property_type_list.append(type(element))
                if isinstance(element, container_types):
                    container_reference_list.append(element)
                    container_to_property_map[future_container_index] = property_index
                    future_container_index += 1
                property_index += 1
                element_index += 1
        container_index += 1



    return {"property_names": property_name_list,
            "property_parents": property_parent_list,
            "property_types": property_type_list,
            "container_references": container_reference_list}