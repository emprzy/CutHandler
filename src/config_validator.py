"""OO logic for validating configuration files."""

import os
import pandas as pd
import pathlib


AUDIO_EXTENSIONS = {
        '.mp3', '.m4a', '.aac', '.ogg', '.oga', '.wma', '.opus', '.ra', '.rm',
        '.flac', '.alac', '.wav', '.aiff', '.ape',
        '.mid', '.midi', '.amr'
    }

VIDEO_EXTENSIONS = {
        '.mp4', '.mkv', '.mov', '.avi', '.webm', '.flv',
        '.m4v',
        '.wmv', '.asf',
        '.mpg', '.mpeg', '.m2v', '.ts', '.m2ts', '.mts',
        '.3gp', '.3g2', '.ogv', '.vob', '.rmvb', '.swf'
    }

MEDIA_EXTENSIONS = AUDIO_EXTENSIONS.union(VIDEO_EXTENSIONS)


class ValidatedConfig:

    def __init__(self, config_path: str): 
        """
        # TODO
        """
        self.config_path = pathlib.Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at the specified path: {self.config_path}."
                "Please check that the path is correct and the file exists.")
        if os.path.splitext(self.config_path)[1].lower() != '.csv':
            raise ValueError(f"Invalid file type. Expected a .csv file, but got '{os.path.splitext(self.config_path)[1].lower()}'")
        self.config_df = pd.read_csv(config_path)


    def _validate_columns(self, *, extra_cols_required: list["str"] = []):
        """Ensure that all necessary columns are present in the config."""
        required_cols = ['timestamp_start', 'timestamp_end', 'file_path'] + extra_cols_required
        missing_cols = set(required_cols) - set(self.config_df.columns)
        missing_cols.discard("file_name")
        if missing_cols:
            raise ValueError(f"Missing required columns in DataFrame: {list(missing_cols)}"
                             "Please ensure all columns are lower case and spelled correctly.")


    def _standardize_timestamps(self): # TODO: add 1.5 sec buffer on either end
        """Standardize the time stamps in config, add columns for start/end second markers."""
        try:
            self.config_df['start_td'] = pd.to_timedelta(self.config_df['timestamp_start'])
            self.config_df['end_td'] = pd.to_timedelta(self.config_df['timestamp_end'])
            self.config_df['start_seconds'] = self.config_df['start_td'].dt.total_seconds()
            self.config_df['end_seconds'] = self.config_df['end_td'].dt.total_seconds()
        except ValueError as e:
            raise ValueError(
                "Failed to parse timestamps. Please ensure all values in timestamp columns "
                "are in a parseable format."
            ) from e
        
        invalid_duration_rows = self.config_df[self.config_df['end_seconds'] <= self.config_df['start_seconds']]
        if not invalid_duration_rows.empty:
            raise ValueError("Invalid timestamp durations found; 'timestamp_end' must occur after 'timestamp_start'.\n"
                             f"Problematic rows:\n{invalid_duration_rows[['timestamp_start', 'timestamp_end']]}")

    def _confirm_file_path_existence(self):
        """Iterative over all files in file_path column, ensure they are all valid paths."""
        invalid_file_paths = {}
        for unique_file_path in set(list(self.config_df['file_path'])):
            current_path = pathlib.Path(unique_file_path)
            if not current_path.exists():
                invalid_file_paths[current_path] = "File not found."
            elif not current_path.is_file():
                invalid_file_paths[current_path] = "Path is a directory, not a file."
            elif current_path.suffix.lower() not in MEDIA_EXTENSIONS:
                invalid_file_paths[current_path] = "File is not a valid video or audio file."

        if invalid_file_paths:
            print("\n")
            for bad_file, reason in invalid_file_paths.items():
                print(f"{bad_file}: {reason}")
            print("\n")
            raise FileNotFoundError("Invalid file paths detected. Please confirm all file_paths correctly point to audio/video files.")
        

    def _add_filename_column(self):
        """Add a file_name column, built out of the file_path column."""
        file_paths = list(self.config_df['file_path'])
        file_names = []
        for file_path in file_paths:
            path = pathlib.Path(file_path)
            file_names.append(path.stem)
        self.config_df['file_name'] = file_names


    def _add_unique_index_column(self):
            """Add a unique index for each entry in config file."""
            start_times = self.config_df['start_seconds'].astype(int).astype(str).str.zfill(6)
            end_times = self.config_df['end_seconds'].astype(int).astype(str).str.zfill(6)
    
            self.config_df['unique_index'] = '_CH_' + start_times + '-' + end_times

