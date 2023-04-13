import os

os.system("pip uninstall bsipack -y")
os.system("python setup.py bdist_wheel")
os.system(f"pip install dist\\{os.listdir('dist')[0]}")

# Clean
os.remove("dist")
os.remove("bsipack.egg-info")
try: os.remove("build")
except: pass