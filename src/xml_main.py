"""Entry point for cuthandler-xml"""

import argparse

from config_validator import ValidatedConfig
from xmler import group_and_xml


def main():
    """CutHandler (encode as XML file(s) main execution function)"""

    parser = argparse.ArgumentParser(description = "Clip frisbee videos into XML-encoded information for use in Adobe Premiere.")
    parser.add_argument("-c", "--config-path",
                        type = str,
                        help = "Path to .csv configuration file.",
                        required = True)
    parser.add_argument("-o", "--output-path",
                        type = str,
                        help = "Top-level path to start saving clips to.",
                        required = True)
    args = parser.parse_args()

    # Validate and standardize config, ensure presence of all file_paths
    validated_config_object = ValidatedConfig(args.config_path, "xml")
    validated_config_object._validate_columns()
    validated_config_object._standardize_timestamps()
    validated_config_object._confirm_file_path_existence()
    validated_config_object._add_filename_column()
    validated_config_object._add_unique_index_column()
    config = validated_config_object.config_df

    # Use xmler to encode clippings; one XML file per file in config
    group_and_xml(
        config=config,
        base_output_path=args.output_path
    )


if __name__ == "__main__":
    main()
