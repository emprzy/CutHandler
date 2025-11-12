# CutHandler 🥏 ✂️
The ultimate auto-clipping tool! 

Installation of the `cuthandler` package will make two distinct command line commands available for **lossless(!)** and speedy clipping of your footage:
* `cuthandler-clip` which will clip your source video(s) into individual video files, and
* `cuthandler-xml` which will encode clippings from your source video(s) into XML files that can be imported and used as a sequence in Adobe Premiere Pro or Final Cut Pro, where all of the clips have full handles.

## Installation 
<small>...version 0.1.0...better installation coming soon</small>

#### 1. Clone CutHandler GitHub repository 
In order to utilize CutHandler, you will have to have a local "clone" of all of the code on your machine. This can be done via the command line with Git ([install Git on your machine](https://git-scm.com/install/mac)).
* Open a terminal window
* Navigate to the directory where you would like to store your clone of CutHandler
* Ensure you have Git correctly installed by running `git --version`
* Run this Git command:
```bash
git clone https://github.com/emprzy/CutHandler.git
```

If you have never cloned a GitHub repository with Git before, you can refer to this [documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for more details.
If you have never used the command line before, the only thing you'll need to learn for this step is how to open terminal (search 'terminal' on your machine), and how to [switch between directories](https://www.ibm.com/docs/en/aix/7.1.0?topic=directories-changing-another-directory-cd-command).

#### 2. Install the CutHandler package via command line
Once you have the code on your machine, you must install the package that will allow you to use the commands easily and effectiely. CutHandler offers installation scripts for Linux, Mac, and Windows operating systems. Navigate to the `CutHandler` directory on your machine, and run: 
(Mac and Linux)
```bash
./install-CutHandler.sh
```

(Windows)
```bat
.\install-CutHandler.bat
```

(via command line) at the top-level of your local CutHandler repository. This script will ensure you have necessary dependencies to execute `cuthandler-clip` and `cuthandler-xml` commands. 

## Configuration file set-up

All executions of CutHandler require you to have a valid **configuration file**. Configuration files are the `.csv` instructions that tell CutHandler which videos you would like to be clipped, and what timestamps you would like them to be clipped at – each row represents one clipping. They are very simple to make, and only require the following three columns:

| Column name (**case-sensitive!**) | Description |
|---------------------------------|-------------|
| `timestamp_start` | The start time of clip, in a recognized datetime format (in cut) |
| `timestamp_end` | The end time of the clip, in a recognized datetime format (out cut) | 
| `file_path` | The **ABSOLUTE** path to the parent video file to be clipped from | 

Valid configuration files can have more columns, but they are required to have these three **named exactly as you see them here**. A valid configuration file could look like this:

| `timestamp_start` | `timestamp_end` | `file_path` | `highlight_type` | `year` |
|-------------------|-----------------|-------------|------------------|--------|
| `0:00:05` | `0:00:15` | `Users/emily/Documents/videos/frisbee_game.mp4` | huck | 2024 |
| `0:59:58` | `1:02:04` | `Users/emily/Documents/videos/practice_film.mov` | block | 2019 |
| ... | ... | ... | ... | ... |
| `0:13:17` | `0:14:08` | `Users/emily/Desktop/pleiades_v_colorado.mp4` | layout catch | 2025 |

and must be stored for use by CutHandler as a `.csv` file. The use of additional columns may be useful for you during your clipping process, but can also be optionally utilized for file-naming and output-grouping with `cuthandler-clip`.

## `cuthandler-clip` 

`cuthandler-clip` is the command line command to use when you would like CutHandler to store your clips as individual video files (largely, `cuthandler-clip` is frisbee-specific syntactic sugar for [ffmpeg](https://www.ffmpeg.org/)). 

Pro:
* `cuthandler-clip` offers an advanced organization system for files. You can choose how to group the output and how to name the files; electing to sort/name by any column(s) in your configuration file.

Con:
* If you plan to use your clippings for editing where you are likely to want to extend clips longer than their original timestamp in/out cuts, you will have to retrieve a new clip from the parent file. That is, the individual file appraoch does not provide you with "full handles" on either end of the clip. 

`cuthandler-clip` has four command line options (print this in terminal with `cuthandler-clip --help`):

| Command | Description | Required? | Default setting|
|---------|-------------|-----------|-----------|
| `--config-path`, `-c` | Absolute path to your `.csv` config file | Yes | `N/A` |
| `--output-path`, `-o` | Absolute path to where you would like output to be stored | Yes | `N/A` |
| `--custom-output-grouping`, `-cog` | Using columns from your config (and the structure `"{col1}/{col2}/{etc}"`), optionally specify how you would like your output directories to be grouped. | No | `name_of_parent_file/` |
| `--custom-filenaming-template`, `-cft` | Using columns from your config (and the structure `"{col1}_{col2}_{etc}"`), optionally specify how you would like your files to be named. | No | `name_of_parent_file.ext` |

When utilizing `-cog` or `-cft`, be certain to encase your option entry in quotes, and include the `{}` braces shown in the description above. Note that values provided in these options must match (case *and* spelling) columns that exist in your configuration file, and that columns must not contain spaces or hyphens (underscores are fine). An example `cuthandler-clip` command may look like the following:

```bash
cuthandler-clip \
    --config-path "path/to/config.csv" \
    --output-path "path/to/output-directory" \
    --cog "{year}/{highlight_type}" \
    --cft "{tournament}_{game}"
```

Running this command would result in your clippings being sorted into directories first by year, then by highlight type (say, huck or block), and the files being named according to the tournament and game they came from. For example, perhaps you would find a file at:
```bash
path/to/output-directory/2025/huck/nationals_colorado-quarterfinal_0153601607.mp4
```
You will notice the file name `nationals_colorado-quarterfinal__CH_000043-000050.mp4` has a string of numbers tacked on the end; this is the unique timestamp ID `cuthandler-clip` will assign every video file to prevent failures stemming from overlapping file names. **CutHandler will never overwrite pre-existing files, so it will fail if it finds a file with the same name at a certain output path.** The unique timestamp ID suffix will be applied to every output file, regardless of your custom output grouping or file-naming.

## `cuthandler-xml`

## Troubleshooting (coming soon)
* common errors (don't have homebrew, don't have git, python not installed, executable permission denied, XML file can't find your parent files)
* valid date formats for timestamps (more importantly, invalid)
* dep list (Python, Git, Homebrew, ffmpeg/ffprobe, pandas)
* If you can't figure something out, need help troubleshooting, or believe there is an error, please [raise an issue](https://github.com/emprzy/CutHandler/issues/new)!
* Need help pulling raw footage from Ultiworld? [Visit my discussion]().
