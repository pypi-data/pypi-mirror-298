
import subprocess

def parecord(
    output_file, 
    record=False, 
    playback=False, 
    device=None,
    client_name=None,
    stream_name=None,
    volume=None,
    rate=44100,  # Default to 44100 Hz
    format="s16ne",  # Default format
    channels=2,  # Default stereo
    process_time=None,
    process_time_msec=None,
    raw=False,
    file_format=None,
):
    # Start building the command
    cmd = ["parecord"]

    # Add common flags
    if record:
        cmd.append("--record")
    if playback:
        cmd.append("--playback")
    
    # Server and device options
    if device:
        cmd += ["--device", device]
    
    # Naming options
    if client_name:
        cmd += ["--client-name", client_name]
    if stream_name:
        cmd += ["--stream-name", stream_name]
    
    # Audio configuration options
    if volume:
        cmd += ["--volume", str(volume)]
    if rate:
        cmd += ["--rate", str(rate)]
    if format:
        cmd += ["--format", format]
    if channels:
        cmd += ["--channels", str(channels)]
    if process_time:
        cmd += ["--process-time", str(process_time)]
    if process_time_msec:
        cmd += ["--process-time-msec", str(process_time_msec)]
    
    # File handling options
    if raw:
        cmd.append("--raw")
    if file_format:
        cmd += ["--file-format", file_format]
    
    # Add additional properties if provided
      
    # Add the output file
    cmd.append(output_file)

    # Run the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Some Error Occured: {e}")
        return False
    return True
