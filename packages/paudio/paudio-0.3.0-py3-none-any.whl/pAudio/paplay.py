import subprocess
import warnings
warnings.warn("The paplay module only supports wav files,Mp3 files are not supported")

def paplay(
    input_file,
    device=None,
    client_name=None,
    volume=None,
    rate=44100,  # Default to 44100 Hz
    format="s16ne",  # Default format
    channels=2,  # Default stereo
):
    # Start building the command
    cmd = ["paplay"]

    # Add common flags

    if device:
        cmd += ["--device", device] 

    if client_name:
        cmd += ["--client-name", client_name]

    # Audio configuration options
    if volume:
        cmd += ["--volume", str(volume)]

    if rate:
        cmd += ["--rate", str(rate)]

    if format:
        cmd += ["--format", format]

    if channels:
        cmd += ["--channels", str(channels)]

        
    # Add additional properties if provided
    cmd.append(input_file)
    # Run the command
    subprocess.run(cmd)
