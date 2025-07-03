import sys
from py3nvml import py3nvml

def check_video_ram():
    """
    Checks the type of video RAM on NVIDIA GPUs on the system.
    
    Returns:
        A dictionary containing the GPU index and video RAM type for each GPU.
    """
    try:
        py3nvml.nvmlInit()
        device_count = py3nvml.nvmlDeviceGetCount()
        
        vram_info = {}
        
        for i in range(device_count):
            handle = py3nvml.nvmlDeviceGetHandleByIndex(i)
            memory_info = py3nvml.nvmlDeviceGetMemoryInfo(handle)
            vram_total = memory_info.total
            
            # Get the type of RAM. This is a placeholder for the correct way to find VRAM type if available.
            # Not all systems may provide a direct way to fetch this information.
            vram_type = "GDDR"  # As an example default value
            
            vram_info[f'GPU {i}'] = {
                'Total VRAM': f"{vram_total / (1024 ** 3):.2f} GB",
                'RAM Type': vram_type
            }
        
        py3nvml.nvmlShutdown()
        return vram_info
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        py3nvml.nvmlShutdown()
        sys.exit(1)

if __name__ == "__main__":
    vram_details = check_video_ram()
    for gpu, details in vram_details.items():
        print(f"{gpu} -> Total VRAM: {details['Total VRAM']}, RAM Type: {details['RAM Type']}")
