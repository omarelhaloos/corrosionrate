import pickletools
import os
import sys

# Add src to python path to mimic app behavior
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config.config import MODEL_PATHS

def get_imports(file_path):
    imports = set()
    try:
        with open(file_path, "rb") as f:
            for opcode, arg, pos in pickletools.genops(f):
                if opcode.name == "GLOBAL":
                    module, name = arg.split(" ", 1)
                    imports.add(f"{module}.{name}")
                elif opcode.name == "STACK_GLOBAL":
                    # Stack global is harder to parse without context, skipping for now
                    pass 
    except Exception as e:
        return f"Error reading pickle: {e}"
    return imports

print("---- Inspecting Pickle Imports ----")
for name, path in MODEL_PATHS.items():
    print(f"\nScanning: {name}")
    imports = get_imports(path)
    if isinstance(imports, set):
        for imp in sorted(imports):
            print(f"  - {imp}")
    else:
        print(f"  {imports}")
print("\n---- End Inspection ----")
