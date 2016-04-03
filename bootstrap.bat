virtualenv python_virtualenv --no-site-packages

call python_virtualenv/Scripts/activate.bat

pip install pyOpengl==3.1.0
pip install pysdl2
pip install numpy-1.10.0+mkl-cp27-none-win32.whl
pip install pyrr
pip install pyYaml
pip install pypybox2d
pip install nose
pip install mock
pip install imageio

call python_virtualenv/Scripts/deactivate.bat
