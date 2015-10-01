virtualenv python_virtualenv --no-site-packages

call python_virtualenv/Scripts/activate.bat

pip install pyopengl==3.1.0
pip install pysdl2
pip install pyrr
pip install pyYaml
pip install box2D


call python_virtualenv/Scripts/deactivate.bat
