import traceback
import sys

print("Starting main.py wrapper...")
try:
    import main
    print("Main module imported successfully.")
    import tkinter as tk
    print("Tkinter imported.")
    
    root = tk.Tk()
    print("tk.Tk() initialized.")
    
    from main import AuthApp
    app = AuthApp(root)
    print("AuthApp initialized.")
    
    print("Starting mainloop (will close after 2 seconds)...")
    root.after(2000, root.destroy)
    root.mainloop()
    print("Mainloop finished successfully.")
    
except Exception as e:
    print("--- EXCEPTION CAUGHT ---")
    traceback.print_exc()
    sys.exit(1)
except BaseException as e:
    print("--- BASE EXCEPTION CAUGHT ---")
    traceback.print_exc()
    sys.exit(1)
print("Wrapper finished.")
