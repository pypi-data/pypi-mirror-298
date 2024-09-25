
import subprocess

def parecord(
    output_file, 
    record=False, 
    playback=False, 
    verbose=False,
    server=None,
    device=None,
    client_name=None,
    stream_name=None,
    volume=None,
    rate=44100,  # Default to 44100 Hz
    format="s16ne",  # Default format
    channels=2,  # Default stereo
    channel_map=None,
    fix_format=False,
    fix_rate=False,
    fix_channels=False,
    no_remix=False,
    no_remap=False,
    latency=None,
    process_time=None,
    latency_msec=None,
    process_time_msec=None,
    raw=False,
    passthrough=False,
    file_format=None,
    list_file_formats=False,
    monitor_stream=None,
    additional_properties=None
):
    # Start building the command
    cmd = ["parecord"]

    # Add common flags
    if record:
        cmd.append("--record")
    if playback:
        cmd.append("--playback")
    if verbose:
        cmd.append("--verbose")
    
    # Server and device options
    if server:
        cmd += ["--server", server]
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
    if channel_map:
        cmd += ["--channel-map", channel_map]
    
    # Fix options
    if fix_format:
        cmd.append("--fix-format")
    if fix_rate:
        cmd.append("--fix-rate")
    if fix_channels:
        cmd.append("--fix-channels")
    
    # Mixing options
    if no_remix:
        cmd.append("--no-remix")
    if no_remap:
        cmd.append("--no-remap")
    
    # Latency and process options
    if latency:
        cmd += ["--latency", str(latency)]
    if process_time:
        cmd += ["--process-time", str(process_time)]
    if latency_msec:
        cmd += ["--latency-msec", str(latency_msec)]
    if process_time_msec:
        cmd += ["--process-time-msec", str(process_time_msec)]
    
    # File handling options
    if raw:
        cmd.append("--raw")
    if passthrough:
        cmd.append("--passthrough")
    if file_format:
        cmd += ["--file-format", file_format]
    if list_file_formats:
        cmd.append("--list-file-formats")
    if monitor_stream:
        cmd += ["--monitor-stream", str(monitor_stream)]
    
    # Add additional properties if provided
    if additional_properties:
        for prop, value in additional_properties.items():
            cmd += ["--property", f"{prop}={value}"]
    
    # Add the output file
    cmd.append(output_file)

    # Run the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    return True
