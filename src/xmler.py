import subprocess
import pathlib
import json
import pandas as pd
import xml.etree.ElementTree as ET


def _get_video_properties(file_path: str) -> dict:
    """
    Uses ffprobe to get essential video properties.

    Returns a dictionary with:
    - width (int)
    - height (int)
    - timebase (str, e.g., "24")
    - duration_frames (int)
    - pathurl (str, formatted for XML)
    - file_name (str)
    """
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0', # Only look at the first video stream
        '-show_entries', 'stream=width,height,r_frame_rate,duration_ts',
        '-of', 'json',
        str(file_path)
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)["streams"][0]
        
        timebase = data['r_frame_rate'].split('/')[0]
        duration_frames = int(data['duration_ts'])
        p_path = pathlib.Path(file_path)
        path_url = p_path.as_uri()

        return {
            "width": int(data['width']),
            "height": int(data['height']),
            "timebase": timebase, 
            "duration_frames": duration_frames,
            "pathurl": path_url,
            "file_name": p_path.name
        }
        
    except Exception as e:
        raise RuntimeError(f"Failed to probe video file: {file_path}\nError: {e}")
    

def _create_xml_shell(video_props: dict) -> tuple:
    """
    Creates the main XML structure for a sequence.

    Returns a tuple containing:
    (root, sequence, video_track, audio_track_1, audio_track_2, file_el file_id)
    """

    file_id = "file-1" 
    root = ET.Element("xmeml", version="4")
    sequence = ET.SubElement(root, "sequence")
    seq_name = f"{pathlib.Path(video_props['file_name']).stem}_sequence"
    ET.SubElement(sequence, "name").text = seq_name
    rate = ET.SubElement(sequence, "rate")
    ET.SubElement(rate, "timebase").text = video_props['timebase']
    ET.SubElement(rate, "ntsc").text = "TRUE" 
    media = ET.SubElement(sequence, "media")
    video = ET.SubElement(media, "video")
    v_format = ET.SubElement(video, "format")
    v_sample = ET.SubElement(v_format, "samplecharacteristics")
    ET.SubElement(v_sample, "width").text = str(video_props['width'])
    ET.SubElement(v_sample, "height").text = str(video_props['height'])
    v_rate = ET.SubElement(v_sample, "rate")
    ET.SubElement(v_rate, "timebase").text = video_props['timebase']
    ET.SubElement(v_rate, "ntsc").text = "TRUE"
    video_track = ET.SubElement(video, "track")
    audio = ET.SubElement(media, "audio")
    a_format = ET.SubElement(audio, "format")
    a_sample = ET.SubElement(a_format, "samplecharacteristics")
    ET.SubElement(a_sample, "depth").text = "16"
    ET.SubElement(a_sample, "samplerate").text = "48000"
    audio_track_1 = ET.SubElement(audio, "track")
    audio_track_2 = ET.SubElement(audio, "track")
    file_el = ET.Element("file", id=file_id)
    ET.SubElement(file_el, "name").text = video_props['file_name']
    ET.SubElement(file_el, "pathurl").text = video_props['pathurl']
    f_rate = ET.SubElement(file_el, "rate")
    ET.SubElement(f_rate, "timebase").text = video_props['timebase']
    ET.SubElement(f_rate, "ntsc").text = "TRUE"
    ET.SubElement(file_el, "duration").text = str(video_props['duration_frames'])
    f_media = ET.SubElement(file_el, "media")
    f_video = ET.SubElement(f_media, "video")
    f_v_sample = ET.SubElement(f_video, "samplecharacteristics")
    ET.SubElement(f_v_sample, "width").text = str(video_props['width'])
    ET.SubElement(f_v_sample, "height").text = str(video_props['height'])
    # --- 👇 ADD THIS NEW BLOCK HERE 👇 ---
    f_audio = ET.SubElement(f_media, "audio")
    ET.SubElement(f_audio, "channelcount").text = "2" # Assume stereo
    a_sample = ET.SubElement(f_audio, "samplecharacteristics")
    ET.SubElement(a_sample, "depth").text = "16"
    ET.SubElement(a_sample, "samplerate").text = "48000" # Common default
    # --- 👆 END OF NEW BLOCK 👆 ---
    
    return root, sequence, video_track, audio_track_1, audio_track_2, file_el, file_id


def _add_clip_item(
        parent_track: ET.Element,
        item_id: str,
        master_id: str,
        name: str,
        file_id: str,
        timebase: str,
        start_frame: int,
        end_frame: int,
        in_frame: int,
        out_frame: int,
        ) -> ET.Element:
    """Helper to create a single <clipitem> with all its sub-elements."""
    clip_item = ET.SubElement(parent_track, "clipitem", id=item_id)
    ET.SubElement(clip_item, "masterclipid").text = master_id
    ET.SubElement(clip_item, "name").text = name
    
    # Add rate
    rate = ET.SubElement(clip_item, "rate")
    ET.SubElement(rate, "timebase").text = timebase
    ET.SubElement(rate, "ntsc").text = "TRUE"

    # Timeline and Source In/Out points (as strings)
    ET.SubElement(clip_item, "start").text = str(start_frame)
    ET.SubElement(clip_item, "end").text = str(end_frame)
    ET.SubElement(clip_item, "in").text = str(in_frame)
    ET.SubElement(clip_item, "out").text = str(out_frame)

    # File reference
    ET.SubElement(clip_item, "file", id=file_id)
    
    return clip_item


def _add_links(
    clip_item: ET.Element,
    v_clip_id: str,
    a1_clip_id: str,
    a2_clip_id: str,
    clip_index: int
):
    """Adds the three <link> tags to a clipitem for three necessary source files."""
    
    # Link to Video
    link1 = ET.SubElement(clip_item, "link")
    ET.SubElement(link1, "linkclipref").text = v_clip_id
    ET.SubElement(link1, "mediatype").text = "video"
    ET.SubElement(link1, "trackindex").text = "1"
    ET.SubElement(link1, "clipindex").text = str(clip_index)

    # Link to Audio 1
    link2 = ET.SubElement(clip_item, "link")
    ET.SubElement(link2, "linkclipref").text = a1_clip_id
    ET.SubElement(link2, "mediatype").text = "audio"
    ET.SubElement(link2, "trackindex").text = "1"
    ET.SubElement(link2, "clipindex").text = str(clip_index)
    ET.SubElement(link2, "groupindex").text = "1"

    # Link to Audio 2
    link3 = ET.SubElement(clip_item, "link")
    ET.SubElement(link3, "linkclipref").text = a2_clip_id
    ET.SubElement(link3, "mediatype").text = "audio"
    ET.SubElement(link3, "trackindex").text = "2"
    ET.SubElement(link3, "clipindex").text = str(clip_index)
    ET.SubElement(link3, "groupindex").text = "1"


def group_and_xml(
        config: pd.DataFrame,
        base_output_path: str
    ) -> None:
    """
    Group and encode all video files cited in the configuration file to XML.

    One XML file per video file in config.

    Args:
        config: Validated pd.DataFrame version of the config file
        base_output_path: Base output path where XML file(s) will be saved
    """

    print("Beginning XML encoding process...")

    base_output_path = pathlib.Path(base_output_path)
    base_output_path.mkdir(parents=True, exist_ok=True)
    gbo = config.groupby('file_path')

    encoded_and_saved_file_count = 0
    unencoded_or_unsaved_video_files = {}
    for file_path, df in gbo:
        
        print(f"Encoding file '{df['file_name'].iloc[0]}' from config...")
        file_name_stem = pathlib.Path(df['file_name'].iloc[0]).stem
        output_xml_path = base_output_path / f"{file_name_stem}.xml"
        if output_xml_path.exists():
            print(f"XML file {output_xml_path} already exists in output directory, proceeding with other files.")
            unencoded_or_unsaved_video_files[file_path] = f"XML file {output_xml_path} already exists in output directory. Will not overwrite."
            continue
        try:
            video_props = _get_video_properties(file_path)
            root, sequence, v_track, a_track1, a_track2, file_element, file_id = _create_xml_shell(video_props)
            is_first_clip = True
            current_timeline_frame = 0
            timebase_int = int(video_props['timebase'])


            # Add individual clips to XML
            for clip_index, row in enumerate(df.itertuples(), start=1):
                
                # --- A. Calculate Frame Numbers ---
                # Convert clip start/end times from seconds (float) to frames (int)
                in_frame = int(row.start_seconds * timebase_int)
                out_frame = int(row.end_seconds * timebase_int)
                
                # Calculate timeline placement
                timeline_start_frame = current_timeline_frame
                clip_duration_frames = out_frame - in_frame
                timeline_end_frame = timeline_start_frame + clip_duration_frames

                # --- B. Create Unique IDs ---
                # Use the row's unique_index for consistent, unique IDs
                master_id = f"master-{row.unique_index}"
                v_clip_id = f"v-clip-{row.unique_index}"
                a1_clip_id = f"a1-clip-{row.unique_index}"
                a2_clip_id = f"a2-clip-{row.unique_index}"
                
                # --- C. Create Clip Items ---
                clip_name = video_props['file_name']
                timebase = video_props['timebase']

                # Create Video Clip (V1)
                v_clip = _add_clip_item(
                    parent_track=v_track, item_id=v_clip_id, master_id=master_id,
                    name=clip_name, file_id=file_id, timebase=timebase,
                    start_frame=timeline_start_frame, end_frame=timeline_end_frame,
                    in_frame=in_frame, out_frame=out_frame
                )
                if is_first_clip:
                    # Remove the simple <file id.../> reference
                    file_ref = v_clip.find("file")
                    v_clip.remove(file_ref)

                    # Add the full <file ...>...</file> definition
                    v_clip.append(file_element)
                    is_first_clip = False
                
                # Create Audio Clip 1 (A1)
                a1_clip = _add_clip_item(
                    parent_track=a_track1, item_id=a1_clip_id, master_id=master_id,
                    name=clip_name, file_id=file_id, timebase=timebase,
                    start_frame=timeline_start_frame, end_frame=timeline_end_frame,
                    in_frame=in_frame, out_frame=out_frame
                )
                # Add audio-specific tag
                ET.SubElement(a1_clip, "sourcetrack").text = "1"
                
                # Create Audio Clip 2 (A2)
                a2_clip = _add_clip_item(
                    parent_track=a_track2, item_id=a2_clip_id, master_id=master_id,
                    name=clip_name, file_id=file_id, timebase=timebase,
                    start_frame=timeline_start_frame, end_frame=timeline_end_frame,
                    in_frame=in_frame, out_frame=out_frame
                )
                # Add audio-specific tag
                ET.SubElement(a2_clip, "sourcetrack").text = "2"

                # --- D. Link the clips together ---
                _add_links(v_clip, v_clip_id, a1_clip_id, a2_clip_id, clip_index)
                _add_links(a1_clip, v_clip_id, a1_clip_id, a2_clip_id, clip_index)
                _add_links(a2_clip, v_clip_id, a1_clip_id, a2_clip_id, clip_index)

                # --- E. Update Timeline "Playhead" ---
                # Move the playhead to the end of the clip we just added
                current_timeline_frame = timeline_end_frame
            
            # --- END OF NEW LOGIC ---


            # Set the final sequence duration
            ET.SubElement(sequence, "duration").text = str(current_timeline_frame)
            # Write the XML file
            output_xml_path = base_output_path / f"{file_name_stem}.xml"
            tree = ET.ElementTree(root)
            tree.write(output_xml_path, encoding="UTF-8", xml_declaration=True)
            with open(output_xml_path, 'r+') as f:
                content = f.read()
                f.seek(0,0)
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n' + content.split('\n', 1)[-1])
            encoded_and_saved_file_count += 1

        except Exception as e:
            unencoded_or_unsaved_video_files[file_path] = e
            print(f"Unable to encode file {file_path} to XML, proceeding with other files.")
            continue
    

    print(f"XML encoding process complete.") 
    print(f"Successfully encoded and saved {encoded_and_saved_file_count}/{len(unencoded_or_unsaved_video_files)+encoded_and_saved_file_count} files.")
    if unencoded_or_unsaved_video_files:
        print("Failed to encode:")
        for bad_file, explanation in unencoded_or_unsaved_video_files.items():
            print(f"{bad_file} due to {explanation}")