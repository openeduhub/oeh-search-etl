
"""

blacklist_brandenburg = []
blacklist_thueringen = []
blacklist_niedersachsen = []

# generate permission table

permission_table = ... (publisher_id -> permissions)

sodix_spider_node_id = do_stuff()
nodes = get_all_nodes_inside_sodix_spider()

for node in nodes:
    # check if node['name'] really is a uuid
    publisher_id = node['name']
    try:
        permissions = permission_table[publisher_id]
    except KeyError:
        logging.warning(f'No permissions found for publisher_id: {publisher_id}'
        continue
    set_permission(node['id'], permissions)

"""