import setuptools
import os

# * Функция получения полных путей к файлам в папках и подпапках
def globalizer(dirpath: str) -> list:
    files = []
    folder_abspath = os.path.abspath(dirpath)
    if os.path.isdir(folder_abspath):
        for i in os.listdir(folder_abspath):
            path = folder_abspath + os.sep + i
            if os.path.isdir(path):
                for _i in globalizer(path):
                    files.append(_i)
            elif os.path.isfile(path):
                files.append(path)
    elif os.path.isfile(folder_abspath):
        files.append(folder_abspath)
    return files

# * Ну, setup
setuptools.setup(
	name="bsipack",
	version="0.3.1",
	description='BSI Packages.',
	keywords=['bsipack'],
	packages=setuptools.find_packages(),
	author_email='semina054@gmail.com',
	url="https://github.com/romanin-rf/basic-system-information",
	package_data={ "bsipack": globalizer(os.path.join(os.path.dirname(__file__), "bsipack")) },
	include_package_data=True,
	author='ProgrammerFromParlament',
	license='MIT',
	install_requires=["kivy", "kivymd", "rich", "psutil", "pillow", "dataclasses"],
    setup_requires=["kivy", "kivymd", "rich", "psutil", "pillow", "dataclasses"]
)