# CutHandler 🥏 ✂️
The ultimate auto-clipping tool! Kee

Installation of the `cuthandler` package will make two distinct command line commands available for lossless(!) clipping of your footage:
* `cuthandler-clip` which will clip your source video(s) into individual video files, and
* `cuthandler-xml` which will encode clippings from your source video(s) into XML files that can be imported and used as a sequence in Adobe Premiere Pro or Final Cut Pro, where all of the clips have full handles.

## Installation 
<small>...version 0.1.0...better installation coming soon</small>

#### 1. Download code via Git 
In order to utilize CutHandler, you will have to have a local "clone" of all of the code on your machine. This can be done through the command line with Git ([install Git on your machine](https://git-scm.com/install/mac)).
* Open a terminal window
* Navigate to the directory where you would like to store your clone of CutHandler
* Ensure you have Git correctly installed by running `git --version`
* Run this Git command:
```bash
git clone https://github.com/emprzy/CutHandler.git
```

If you have never cloned a GitHub repository with Git before, you can refer to this [documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for more details.
If you have never used the command line before, the only thing you'll need to learn for this step is how to open terminal (search 'terminal' on your machine), and how to [switch between directories](https://www.ibm.com/docs/en/aix/7.1.0?topic=directories-changing-another-directory-cd-command).

#### 2. Install the `cuthandler` package via command line
Once you have the code on your machine, you must install the package that will allow you to use the commands easily and effectiely. `cuthandler` offers installation scripts for Linux, Mac, and Windows operating systems. On Mac and Linux, you can run:
```bash
chmod +x install-CutHandler.sh
```
```bash
./install-CutHandler.sh
```

On Windows, you can run:
```bat
.\install-CutHandler.bat
```

(via command line) at the top-level of your local CutHandler repository. This script will ensure you have necessary dependencies to execute `cuthandler-clip` and `cuthandler-xml` commands. 

## Configuration file set-up

All executions of CutHandler require you to have a valid **configuration file**. Configuration files are the instructions that tell CutHandler which videos you would like to be clipped, and at what timestamps you would like them to be clipped at – each row represents one individual clip. They are very simple to make, and only require the following three columns:

| Column name (**case-sensitive!**) | Description |
|---------------------------------|-------------|
| `timestamp_start` | The start time of clip, in a recognized datetime format |
| `timestamp_end` | The end time of the clip, in a recognized datetime format | 
| `file_path` | The **ABSOLUTE** path to the parent video file to be clipped from | 

Valid configuration files can have more columns, but they are required to have these three **named exactly as you see them here**. An

## `cuthandler-clip` 

## `cuthandler-xml`

## Troubleshooting (coming soon)
* common errors
* valid date formats for timestamps
* dep list
* raise an issue if you need
