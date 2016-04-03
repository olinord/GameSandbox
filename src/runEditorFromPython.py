

if __name__ == '__main__':
	import sys
	import os
	os.environ['PYSDL2_DLL_PATH'] = os.path.abspath(os.curdir)
	from editor import EditorApp
	app = EditorApp()
	if app.SetupApp(800, 600):
		app.Run()
