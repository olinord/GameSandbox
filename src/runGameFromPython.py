

if __name__ == '__main__':
    import sys
    import os
    os.environ['PYSDL2_DLL_PATH'] = os.path.abspath(os.curdir)
    from main import RunApp
    RunApp()
