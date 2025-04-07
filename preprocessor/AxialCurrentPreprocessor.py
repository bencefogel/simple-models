import pandas as pd
import numpy as np

from preprocessor.utils.preprocess_axial import get_segment_iax, update_root_node


class AxialCurrentPreprocessor:
    """
    Initializes the AxialCurrentPreprocessor class.

    Initializes two primary DataFrames:
    - axial_current: Stores calculated axial currents with a MultiIndex.
    - axial_current_soma_merged: Stores axial current dataframe with merged somatic section.
    """
    def __init__(self) -> None:
        self.axial_current = pd.DataFrame
        self.axial_current_soma_merged = pd.DataFrame

    def calculate_axial_currents(self, simulation_data: dict) -> None:
        """
        Calculates axial currents based on simulation data.

        Args:
            simulation_data (dict): A dictionary containing connection data and membrane potential data.
                - 'connections': A DataFrame with 'ref', 'par', and 'ri_par' columns.
                - 'membrane_potential_data': A tuple containing segments and membrane potential values.

        Populates the 'axial_current' attribute with a MultiIndex DataFrame of calculated currents.
        """
        connections = simulation_data['connections']
        segments = simulation_data['membrane_potential_data'][0]
        membrane_potential = simulation_data['membrane_potential_data'][1]

        df_v = pd.DataFrame(data=membrane_potential)
        df_v.insert(0, 'segment', segments)

        # Calculate axial currents
        iax = np.empty((connections.shape[0], df_v.shape[1] - 1))
        for i, _ in enumerate(connections.iloc[:, 0]):
            try:
                ref = connections.iloc[i, 0]
                par = connections.iloc[i, 1]
                ri_par = connections.iloc[i, 2]

                v_ref = df_v[df_v['segment'] == ref].iloc[0, 1:].values
                v_par = df_v[df_v['segment'] == par].iloc[0, 1:].values

                iax_row = (v_par - v_ref) / ri_par
            except IndexError:
                # print(f"The following segment does not have a parent: {connections.iloc[i, 0]}")  # sanity check
                iax_row = np.zeros(df_v.shape[1] - 1)
            iax[i, :] = iax_row
        axial_values = iax
        axial_index = pd.DataFrame(data={'ref': connections['ref'].values, 'par': connections['par'].values})

        # Create a DataFrame with a MultiIndex
        multiindex = pd.MultiIndex.from_frame(axial_index)
        self.axial_current = pd.DataFrame(data=axial_values, index=multiindex)

    def merge_section_iax(self, target: str) -> pd.DataFrame:
        """
        Merges axial currents for a specified target section ('soma' or 'dendrite').

        Args:
            target (str): The target section to merge ('soma' or a specific 'dend' name).

        Returns:
            pd.DataFrame: The merged axial current DataFrame.
        """
        if target.startswith('soma'):
            return self.merge_soma_iax()
        elif target.startswith('dend'):
            self.merge_soma_iax()
        return self.merge_dendrite_iax(target)

    def merge_soma_iax(self) -> pd.DataFrame:
        """no merging implemented currently"""
        df = self.axial_current
        return df

    def merge_dendrite_iax(self, target: str) -> pd.DataFrame:
        """
        Merges dendrite-related axial currents for a specified target dendrite section.

        Args:
            target (str): The target dendrite section to merge.

        Returns:
            pd.DataFrame: The updated axial current DataFrame for the specified dendrite section (with updated root node).
        """

        df = self.axial_current_soma_merged
        # Select external iax connections (between parent and children nodes)
        df_segment_ref = df[df.index.get_level_values('ref').str.startswith(
            f'{target}(')]  # select iax rows where segment is the reference
        df_segment_par = df[df.index.get_level_values('par').str.startswith(
            f'{target}(')]  # select iax rows where segment is the parent
        # this is now a new copy - so renaming does not affects the original dataframe
        df_external = pd.concat([df_segment_ref, df_segment_par]).drop_duplicates(
            keep=False)  # this keeps rows that are unique (meaning that they connect to external nodes)

        # Rename index
        iref = df.index.get_level_values('ref').str.startswith(f'{target}(')
        first_internal_name = df.index.get_level_values('ref')[iref].sort_values()[
            0]  # we assume that sorting will sort it correctly: The first element is the first internal node
        last_terminal_name = df.index.get_level_values('ref')[iref].sort_values()[
            -1]  # and the last is the terminal node
        rename_dict = {first_internal_name: target,
                       last_terminal_name: target}
        df_external.rename(index=rename_dict, level='ref', inplace=True)
        df_external.rename(index=rename_dict, level='par', inplace=True)

        # Remove segment iax rows (both external and internal)
        df_internal_idx = pd.concat([df_segment_ref, df_segment_par]).drop_duplicates().index
        df.drop(df_internal_idx, inplace=True)

        # Concatenate updated external iax rows
        df_merged = pd.concat([df, df_external])
        df_updated_root = update_root_node(df_merged, target)
        return df_updated_root
