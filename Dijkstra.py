Implementing Edge Addition to the Graph
1. Edge Addition Logic:
Here's the conceptual logic for adding edges between picking and stacking nodes (and potentially between stacking nodes if allowing multi-level stacks):
def add_edges(graph):
    stacking_nodes = [node for node in graph.nodes if graph.nodes[node]['type'] == 'stacking']
    picking_nodes = [node for node in graph.nodes if graph.nodes[node]['type'] == 'picking']

    for picking_node in picking_nodes:
        box_id = graph.nodes[picking_node]['box_id']
        box_size = graph.nodes[picking_node]['box_size']

        for stacking_node in stacking_nodes:
            # Check if the boxes are compatible for stacking (e.g., size constraints)
            if is_compatible_for_stacking(box_id, box_size, stacking_node):
                # Check if stacking is physically possible (e.g., no collisions, reach limitations)
                if is_stacking_possible(picking_node, stacking_node):
                    cost = calculate_edge_cost(picking_node, stacking_node)
                    graph.add_edge(picking_node, stacking_node, cost=cost)
            # 1. Image Capture and Preprocessing
            depth_img, color_img = camera_op.obtain_images()
            depth_img, color_img = pre_proc.crop_images_to_table(depth_img, color_img)
            # ... (save images if needed) ...

            # 2. Object Detection (YOLOv5)
            # ... (run YOLOv5 detection, get bounding box coordinates) ... 

            # 3. Post-Processing and Box Information
            box_coordinates_list = post_proc.pull_coordinates(file_path)
            heights = post_proc.get_obj_height(depth_img, box_coordinates_list)
            real_world_coords = post_proc.pixel_conversion(box_coordinates_list, heights)
            # Create a dictionary to store box information (including stacked status)
            box_dict = {
                i: {
                    'coordinates': real_world_coords[i],
                    'size': calculate_box_size(box_coordinates_list[i]), # Implement this function
                    'stacked': False 
                } for i in range(len(box_coordinates_list))
            }

            # 4. Graph Creation and Updates
            graph = nx.Graph() # Or use your custom graph implementation
            robot_node_id = add_robot_node(graph, robot.getl()) # Function to add robot node
            
            # Add picking and stacking nodes for each box
            for box_id, box_info in box_dict.items():
                if not box_info['stacked']:
                    picking_node_id = add_picking_node(graph, box_id, box_info['coordinates'], box_info['size'])
                    add_stacking_nodes(graph, box_id, box_info['coordinates'], box_info['size'])
                    graph.add_edge(robot_node_id, picking_node_id, cost=calculate_edge_cost(robot_node_id, picking_node_id))
            
            # Add edges between picking and stacking nodes (and stacking to stacking if applicable)
            # ... (implement logic considering size compatibility and stability) ...

            # 5. Shortest Path Calculation and Robot Actions
            start_node = robot_node_id
            end_node =  # Choose any stacking node on the base box 
            shortest_path = nx.dijkstra_path(graph, start_node, end_node, weight=calculate_edge_cost)
            
            # Interpret the path and execute robot actions
            boxes_to_stack = []
            for i in range(len(shortest_path) - 1):
                # ... (similar logic as the previous example, handling robot movement, 
                # picking, stacking, and updating box_dict['stacked'] status) ... 

            # 6. Check for Completion 
            if all(box_info['stacked'] for box_info in box_dict.values()):
                break # All boxes stacked, exit loop

        except Exception as e:
            # ... (handle exceptions and errors) ...

    # ... (clean up and exit) ... 