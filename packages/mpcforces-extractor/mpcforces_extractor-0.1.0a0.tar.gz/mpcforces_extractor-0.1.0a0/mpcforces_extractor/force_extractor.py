import os
import time
from typing import Dict
import networkx as nx
from mpcforces_extractor.reader.modelreaders import FemFileReader
from mpcforces_extractor.reader.mpcforces_reader import MPCForcesReader
from mpcforces_extractor.datastructure.entities import Element
from mpcforces_extractor.datastructure.loads import Force, Moment
from mpcforces_extractor.visualize.tcl_visualize import VisualizerConnectedParts


class MPCForceExtractor:
    """
    This class is used to extract the forces from the MPC forces file
    and calculate the forces for each rigid element by property
    """

    def __init__(self, fem_file_path, mpc_file_path, output_folder: str):
        self.fem_file_path: str = fem_file_path
        self.mpc_file_path: str = mpc_file_path
        self.output_folder: str = output_folder
        self.reader: FemFileReader = None
        self.part_id2connected_node_ids: Dict = {}

        # create output folder if it does not exist, otherwise delete the content
        if os.path.exists(output_folder):
            for file in os.listdir(output_folder):
                file_path = os.path.join(output_folder, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
        else:
            os.makedirs(output_folder, exist_ok=True)

    def get_part_id2node_ids_graph(self, graph: nx.Graph) -> Dict:
        """
        This method is used to get the part_id2node_ids using the graph
        """
        start_time = time.time()
        print("Building the part_id2node_ids using the graph")
        part_id2node_ids = {}

        print("...Calculating connected components")
        connected_components = list(nx.connected_components(graph))

        print(
            "Finished calculating the connected components, returning part_id2node_ids"
        )
        print("..took ", round(time.time() - start_time, 2), "seconds")

        for i, connected_component in enumerate(connected_components):
            part_id2node_ids[i + 1] = [node.id for node in connected_component]

        return part_id2node_ids

    def get_mpc_forces(self, block_size: int) -> dict:
        """
        This method reads the FEM File and the MPCF file and extracts the forces
        in a dictory with the rigid element as the key and the property2forces dict as the value
        """
        self.reader = FemFileReader(self.fem_file_path, block_size)
        print("Reading the FEM file")
        start_time = time.time()
        self.reader.create_entities()

        print("..took ", round(time.time() - start_time, 2), "seconds")
        print("Building the mpcs")
        start_time = time.time()
        self.reader.get_rigid_elements()
        print("..took ", round(time.time() - start_time, 2), "seconds")

        self.reader.get_loads()
        # Element.get_neighbors()

        mpc2forces = {}

        # Get the connected Nodes for all nodes
        graph = Element.graph.copy()
        self.part_id2connected_node_ids = self.get_part_id2node_ids_graph(graph)

        for mpc in self.reader.rigid_elements:
            node2forces = MPCForcesReader(self.mpc_file_path).get_nodes2forces()

            part_id2forces = mpc.sum_forces_by_connected_parts(
                node2forces, self.part_id2connected_node_ids
            )
            mpc2forces[mpc] = part_id2forces

            part_id2node_ids = mpc.part_id2node_ids
            # write it to the file
            file_path_out = os.path.join(
                self.output_folder, f"RigidElement_{mpc.element_id}.txt"
            )
            with open(file_path_out, "w", encoding="utf-8") as file:
                file.write(f"MPC Element ID: {mpc.element_id}\n")
                file.write(f"  MPC Config: {mpc.mpc_config}\n")
                master_node = mpc.master_node
                file.write(f"  Master Node ID: {master_node.id}\n")
                file.write(f"  Master Node Coords: {master_node.coords}\n")

                file.write(f"  Slave Nodes: {len(mpc.nodes)}\n")
                file.write(f"  Parts: {len(part_id2node_ids)}\n")
                for part_id in sorted(part_id2node_ids.keys()):
                    node_ids = part_id2node_ids[part_id]
                    file.write(f"  Part ID: {part_id}\n")

                    file.write(f"    Slave Nodes: {len(node_ids)}\n")
                    node_ids_str = ", ".join([str(node_id) for node_id in node_ids])
                    file.write(f"    {node_ids_str}\n")

        return mpc2forces

    def write_suammry(self, mpc_element2part2forces: dict):
        """
        This method writes the summary of the forces extracted from the MPC forces file
        """
        start_time = time.time()

        file_path_out = os.path.join(self.output_folder, "summary.txt")

        timestamp = time.time()
        local_time = time.localtime(timestamp)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

        with open(file_path_out, "w", encoding="utf-8") as file:
            file.write("Summary of the MPC forces extraction\n")
            file.write(f"Date: {formatted_time}\n")
            file.write(f"Input FEM file: {self.fem_file_path}\n")
            file.write(f"Input MPC forces file: {self.mpc_file_path}\n")
            file.write("\n")

            for mpc, part_id2forces in mpc_element2part2forces.items():
                file.write(f"Rigid Element ID: {mpc.element_id}\n")
                file.write(f"  MPC Config: {mpc.mpc_config.name}\n")

                # Forces present
                for _, load in FemFileReader.load_id2load.items():
                    load_x = round(load.compenents[0], 3)
                    load_y = round(load.compenents[1], 3)
                    load_z = round(load.compenents[2], 3)
                    # check if load is instance of force or a moment
                    load_type = "None"
                    if isinstance(load, Force):
                        load_type = "Force"
                    if isinstance(load, Moment):
                        load_type = "Moment"

                    if load.node_id in [mpc.master_node.id]:
                        file.write(
                            f"  {load_type} at Master ID: {load.id}; {load_x},{load_y},{load_z}\n"
                        )
                    if load.node_id in [node.id for node in mpc.nodes]:
                        file.write(
                            f"  {load_type} at Slave ID: {load.id}; {load_x},{load_y},{load_z}\n"
                        )

                # 1D elements associated with the master node
                for element1D in self.reader.elements_1D:
                    if mpc.master_node in [element1D.node1, element1D.node2]:
                        file.write(
                            f"  1D Element ID: {element1D.id} associated with the master Node\n"
                        )

                master_node = mpc.master_node
                file.write(f"  Master Node ID: {master_node.id}\n")
                file.write(f"  Master Node Coords: {master_node.coords}\n")

                file.write(f"  Slave Nodes: {len(mpc.nodes)}\n")
                for part_id in sorted(part_id2forces.keys()):
                    number_of_slave_nodes = len(mpc.part_id2node_ids[part_id])
                    if number_of_slave_nodes == 0:
                        continue
                    forces = part_id2forces[part_id]
                    file.write(f"  Part ID: {part_id}\n")
                    node_ids = mpc.part_id2node_ids[part_id]
                    file.write(
                        f"    First 5 Slave Nodes for Location {node_ids[1:6]}\n"
                    )
                    file.write(f"    Slave Nodes: {len(node_ids)}\n")
                    force_names = ["FX", "FY", "FZ", "MX", "MY", "MZ"]
                    for force, force_name in zip(forces, force_names):
                        file.write(f"    {force_name}: {force:.3f}\n")
                file.write("\n")

        print("Summary written to", file_path_out)
        print("..took ", round(time.time() - start_time, 2), "seconds")

    def write_tcl_vis_lines(self):
        """
        This method writes the tcl visualization lines
        """

        start_time = time.time()

        output_vis = os.path.join(self.output_folder, "tcl_visualization")
        visualizer = VisualizerConnectedParts(
            self.part_id2connected_node_ids, output_vis
        )
        visualizer.output_tcl_lines_for_part_vis()

        print("TCL visualization lines written to", output_vis)
        print("..took ", round(time.time() - start_time, 2), "seconds")
