"""Documentation"""


import subprocess
import pathlib
import pandas as pd


def group_and_clip(
        config: pd.DataFrame, 
        output_grouping_columns: list[str], 
        file_naming_columns: list[str], 
        base_output_path: str,
    ) -> None:
    """
    Group and clip all video files cited in the configuration file.

    Args:
        config: Validated pd.DataFrame version of the config file
        output_grouping_columns: 
            Columns to be used in custom output grouping hierarchy 
            (default is aggregating by name of file being clipped from)
        file_naming_columns: 
            Columns to be used in custom file name structure 
            (default is the name of the file being clipped from)
        base_output_path: Base output path where XML file(s) will be saved
    """
    
    print("Beginning clipping process...")

    base_output_path = pathlib.Path(base_output_path)
    filename_template = "_".join([f"{{{col}}}" for col in file_naming_columns])
    output_template = "/".join([f"{{{col}}}" for col in output_grouping_columns])
    grouped_data = config.groupby(output_grouping_columns)

    unclipped_files_due_to_preexisting_file_path = []
    for _, group_df in grouped_data:
        first_row_in_group = group_df.iloc[0]
        output_directory = base_output_path / pathlib.Path(output_template.format(**first_row_in_group.to_dict()))
        output_directory.mkdir(parents=True, exist_ok=True)

        for row in group_df.itertuples(): 
            row_dict = row._asdict()
            base_name = filename_template.format(**row_dict)

            # Save clips individually with ffmpeg
            file_ext = pathlib.Path(row.file_path).suffix
            output_filename = f"{base_name}_{row.unique_index}{file_ext}" 
            output_path = output_directory / output_filename
            if output_path.exists():
                unclipped_files_due_to_preexisting_file_path.append(str(output_path))
                continue

            start_time = row.start_seconds
            end_time = row.end_seconds

            command = [ # TODO: parallel processing for these to make it faster?
                'ffmpeg',
                '-n', # do not overwrite any pre-existing files
                '-hide_banner', # hides mass output      
                '-loglevel', 'error', # except for errors
                '-ss', str(start_time),
                '-i', row.file_path, # confirm this is a safe flag
                '-to', str(end_time),
                '-c', 'copy', 
                output_path 
            ]

            try:
                subprocess.run(command, check=True, timeout=480) # time out after 8 min, if it is hanging or spinning
            except subprocess.TimeoutExpired:
                raise subprocess.TimeoutExpired(f"Time out error: ffmpeg took too long to process config file row {row.index}.")
            except subprocess.CalledProcessError as e:
                raise subprocess.CalledProcessError(f"Failed on config row {row.index} with error: {e}")

    
    print(f"Clipping process completed for {len(config) - len(unclipped_files_due_to_preexisting_file_path)}/{len(config)} clips.")

    if unclipped_files_due_to_preexisting_file_path:
        print("WARNING, UNABLE TO SAVE FILE(S):\n")
        for bad_file_path in unclipped_files_due_to_preexisting_file_path:
            print(bad_file_path)
            print("\n")
        print("DUE TO THE FACT THAT A FILE ALREADY EXISTS AT THIS PATH.")
        print("PLEASE RESOLVE CONFLICTS AND TRY AGAIN.")

            
