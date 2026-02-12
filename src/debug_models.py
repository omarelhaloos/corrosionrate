import os
import sys
import joblib
import traceback

# Add src to python path to mimic app behavior
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from config.config import MODEL_PATHS
except ImportError:
    # If run from root, current_dir is src/
    sys.path.append(os.path.join(current_dir, '..'))
    from config.config import MODEL_PATHS

with open("debug_log_v2.txt", "w", encoding='utf-8') as f:
    f.write("---- Debugging Model Inspection ----\n")
    for name, path in MODEL_PATHS.items():
        msg = f"Loading: {name}\n"
        print(msg.strip())
        f.write(msg)
        try:
            obj = joblib.load(path)
            obj_type = type(obj)
            module_name = getattr(obj_type, "__module__", "unknown")
            class_name = getattr(obj_type, "__name__", "unknown")
            
            info = f"  - Type: {module_name}.{class_name}\n"
            print(info.strip())
            f.write(info)

            # If it's a pipeline or has steps, inspect them too
            if hasattr(obj, "steps"):
                 for step_name, step_obj in obj.steps:
                     step_type = type(step_obj)
                     step_info = f"    - Step '{step_name}': {step_type.__module__}.{step_type.__name__}\n"
                     print(step_info.strip())
                     f.write(step_info)

        except Exception as e:
            msg = f"❌ Failed to load {name}: {e}\n"
            print(msg.strip())
            f.write(msg)
            traceback.print_exc(file=f)
    f.write("---- End Debugging ----\n")
