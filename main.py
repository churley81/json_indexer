import indexer

json_string = """
  {
    "conversations": "hi"
  }
"""

print(indexer.Indexed(json_string).property_names)