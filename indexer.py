import json

class Indexed:
    def __init__(self, json_string):
        indexed = index_object(json_string)
        self.property_names = indexed['property_names']
        self.property_parents = indexed['property_parents']
        self.container_names = indexed['container_names']
        self.container_parents = indexed['container_parents']
        self.container_references = indexed['container_references']

class InvalidJSONForIndexingError(Exception):
      pass

def index_object(json_string):

    data = json.loads(json_string)
    if not isinstance(data, dict):
        raise InvalidJSONForIndexingError

    container_types = (tuple, list, dict)
    container_name_list = []
    container_reference_list = []
    container_parent_list = []
    property_parent_list = []
    property_name_list = []
    future_container_index = 1
    container_index = 0

    container_reference_list.append(data)
    container_parent_list.append(0)
    container_name_list.append("")

    while container_index < future_container_index:
        parent_container_name = container_name_list[container_index]
        container = container_reference_list[container_index]
        if not isinstance(container, list):
            base_keys = container.keys()
            for key in base_keys:
                if isinstance(container[key], container_types):
                    container_name_list.append(parent_container_name + '/' + str(key))
                    container_parent_list.append(container_index)
                    container_reference_list.append(container[key])
                    future_container_index += 1
                else:
                    property_parent_list.append(container_index)
                    property_name_list.append(key)
        else:
            parent_container_name = parent_container_name + '/' + "Array"
            element_index = 0
            for element in container:
                if isinstance(element, container_types):
                    container_name_list.append(parent_container_name + '/' + str(element_index))
                    container_parent_list.append(container_index)
                    container_reference_list.append(element)
                    future_container_index += 1
                    element_index += 1
                else:
                    pass
        container_index += 1
    return {"property_names": property_name_list,
            "property_parents": property_parent_list,
            "container_names": container_name_list,
            "container_parents": container_parent_list,
            "container_references": container_reference_list}