import subprocess


def get_gpu_info():
    """
    Retrieves the video RAM (VRAM) information for the primary GPU on the system.

    Returns:
        str: A string with the GPU name and total VRAM, or an error message if retrieval fails.
    """
    try:
        # Execute a command to get GPU info using nvidia-smi
        process = subprocess.Popen(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            return f"Error retrieving GPU information: {error.decode('utf-8')}."

        # Decode the output and extract GPU information
        gpu_info = output.decode('utf-8').strip()
        return f"GPU Information: {gpu_info}"

    except FileNotFoundError:
        return "nvidia-smi command not found. Ensure that your GPU drivers are installed and nvidia-smi is available."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}."


def main():
    gpu_info = get_gpu_info()
    print(gpu_info)


if __name__ == "__main__":
    main()
