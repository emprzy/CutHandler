import argparse


from parse_custom_naming_strings import extract_template_keys, validate_template_syntax
from config_validator import ValidatedConfig
from clipper import group_and_clip


# TODO: have message with example command and help info printed at beginning?
# display_intro_message()


def main(): 
    """CutHandler main execution function"""

    parser = argparse.ArgumentParser(description = "Clip frisbee film/videos with CutHandler.") 
    parser.add_argument("-c", "--config-path",
                        type = str,
                        help = "Path to .csv configuration file.",
                        required = True)
    parser.add_argument("-o", "--output-path",
                        type = str,
                        help = "Top-level path to start saving clips to.",
                        required = True)
    parser.add_argument("-cft", "--custom-filename-template",
                        type = str,
                        help = "Using column names from the configuration file, optionally specify an output filename template in the following format '{col1}_{col2}_{col3}', be sure to type the quotations, brackets, underscores, and correct cases. File extension and index will be added automatically. Default is the name of the file to be clipped from, followed by the timestamp index.",
                        default = "{file_name}", 
                        required = False)
    parser.add_argument("-cog", "--custom-output-grouping",
                        type = str,
                        help = "Using column names from the configuration file, optionally specify an output directory structure in the following format '{file_path}/{highlight_type}/{player}', be sure to type the quotations, brackets, slashes, and correct cases. Default is grouping by name of the file to be clipped from.",
                        default = "{file_name}",
                        required = False)
    parser.add_argument("--xml", 
                        action="store_true", 
                        help="If provided, instructs CutHandler to clip footage into an Adobe Premiere Pro sequence.",
                        required = False)
    args = parser.parse_args()

    # First check to validate template syntax
    validate_template_syntax(args.custom_filename_template)
    validate_template_syntax(args.custom_output_grouping)

    # Extract column names from optional file naming template, second template syntax check
    file_naming_columns = []
    file_naming_columns += extract_template_keys(args.custom_filename_template)
    if not file_naming_columns:
        raise ValueError(
            f"Invalid custom filename template: '{args.custom_filename_template}. "
            "Involved columns must be in format '{col1}_{col2}...' and contain no spaces, hyphens, or special characters.")

    # Extract column names from optional output grouping template, second template syntax check
    output_grouping_columns = []
    output_grouping_columns += extract_template_keys(args.custom_output_grouping)
    if not output_grouping_columns:
        raise ValueError(
            f"Invalid custom output grouping template: '{args.custom_output_grouping}. "
            "Involved columns must be in format '{col1}/{col2}...' and contain no spaces, hyphens, or special characters.")


    # Validate and standardize config, ensure presence of all file_paths 
    validated_config_object = ValidatedConfig(args.config_path)
    validated_config_object._validate_columns(extra_cols_required=list(set(file_naming_columns+output_grouping_columns))) 
    validated_config_object._standardize_timestamps()
    validated_config_object._confirm_file_path_existence()
    validated_config_object._add_filename_column()
    validated_config_object._add_unique_index_column()
    config = validated_config_object.config_df

    # Iteratively clip from all files 
    xml = args.xml
    group_and_clip(
        config=config, 
        output_grouping_columns=output_grouping_columns,
        file_naming_columns=file_naming_columns,
        base_output_path=args.output_path,
        xml=xml)



if __name__ == "__main__":
    main()