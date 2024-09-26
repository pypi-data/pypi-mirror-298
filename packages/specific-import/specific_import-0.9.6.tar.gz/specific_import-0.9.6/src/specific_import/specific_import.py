import os
import sys
import inspect
import importlib.util
from pathlib import Path
from typing import List
from types import ModuleType


def get_absolute_path_of_file_doing_importing(frames: List[inspect.FrameInfo]) -> str:
    """
    Returns the absolute path of file doing importing
        :param frames: list of Python frame objects
    """
    index = 0
    current_file_path = __file__
    for index, frame in enumerate(frames):
        if current_file_path == frame.filename:
            break

    try:
        frame_of_file_doing_importing = frames[index + 1]
    except IndexError:
        raise IndexError("The next frame which represents the importing file doesn't exist")

    path = frame_of_file_doing_importing.filename
    return path


def get_absolute_directory_path_of_file_doing_importing(frames: List[inspect.FrameInfo]) -> str:
    """
    Returns the absolute directory of file doing importing
        :param frames: list of Python frame objects
    """
    path = get_absolute_path_of_file_doing_importing(frames)
    return os.path.dirname(path)


def define_path_relative_to_file_doing_importing(resource: str, frames: List[inspect.FrameInfo]) -> str:
    """
    Returns the relative path of file doing importing
        :param resource: absolute file path of module
        :param frames: list of Python frame objects
    """
    path_to_directory_of_file_doing_importing = get_absolute_directory_path_of_file_doing_importing(frames)
    relative_path_of_resource = os.path.join(path_to_directory_of_file_doing_importing, resource)
    absolute_path_of_resource = os.path.abspath(relative_path_of_resource)
    return absolute_path_of_resource


def define_init_file_in_python_package(absolute_file_path_of_target_resource: str) -> str:
    """
    Returns the __init__.py file in a Python package
        :param absolute_file_path_of_target_resource: absolute file path of Python package
    """
    return os.path.join(absolute_file_path_of_target_resource, '../__init__.py')


def get_file_extension(absolute_path_of_resource) -> str:
    """
    Returns file extension
        :param absolute_path_of_resource: absolute file path to module
    """
    _, file_extension = os.path.splitext(absolute_path_of_resource)
    return file_extension


def is_python_package(absolute_path_of_resource: str) -> bool:
    """
    Returns True when path of resource is a folder.

        :param absolute_path_of_resource: absolute file path to module
    """
    return os.path.isdir(absolute_path_of_resource)


def modify_resource_path_for_packages(absolute_path_of_resource: str) -> str:
    """
    Modifies absolute path of module when module is a package. This is needed b/c code must
    account for the init files loading other code.

        :param absolute_path_of_resource: absolute file path to module
    """
    if is_python_package(absolute_path_of_resource):
        absolute_path_of_resource = define_init_file_in_python_package(absolute_path_of_resource)
    return absolute_path_of_resource


def get_resource_spec(absolute_path_of_resource: str):
    """
    Gets the spec file for module

        :param absolute_path_of_resource: absolute file path to module
    """
    spec = importlib.util.spec_from_loader(
        '',
        importlib.machinery.SourceFileLoader(
            '',
            absolute_path_of_resource
        ),
    )
    if spec is None:
        raise ImportError('Resource does not exist.')
    return spec


def module_is_already_loaded(absolute_path_of_resource: str) -> bool:
    """
    Returns True when module has already been loaded

        :param absolute_path_of_resource: absolute file path to module
    """
    return absolute_path_of_resource in sys.modules


def add_module_to_global_modules(absolute_path_of_resource: str, resource_module: ModuleType) -> None:
    """
    This needed so module can be cached for quick reference if re-imported

        :param absolute_path_of_resource: absolute file path to module
        :param resource_module: actual module code in memory
    """
    sys.modules[absolute_path_of_resource] = resource_module


def load_resource_module(resource_module: ModuleType, spec) -> None:
    """
    Load module so it can be used by other code

        :param resource_module: actual module code in memory
    """
    spec.loader.exec_module(resource_module)


def append_to_python_path(absolute_path_to_directory: str) -> None:
    """
    :param absolute_path_to_directory: absolute path to folder
    :return:
    """
    if absolute_path_to_directory in sys.path:
        return
    sys.path.append(absolute_path_to_directory)


def import_file(module_file_path: str) -> ModuleType:
    """
    Returns the module based on its relative of absolute file path name.
    Code considers relativity based on the actual file doing the importing, not the caller.

        :param module_file_path: relative or absolute file path of module.
    """

    frames = inspect.stack()
    absolute_module_file_path = define_path_relative_to_file_doing_importing(module_file_path, frames)
    absolute_module_file_path = modify_resource_path_for_packages(absolute_module_file_path)

    # --------- raise error when absolute module file doesn't exist
    if not os.path.exists(absolute_module_file_path):
        ModuleNotFoundError(f'Could Not Find Module With Path: {absolute_module_file_path}')

    # --------- when module was already loaded, just return that cached result
    if module_is_already_loaded(absolute_module_file_path):
        return sys.modules[absolute_module_file_path]

    # --------- add module's parent folders to Python module path
    path = Path(absolute_module_file_path)
    parent_directory = str(path.parent.absolute())
    append_to_python_path(parent_directory)

    # --------- load module by absolute file path
    spec = get_resource_spec(absolute_module_file_path)
    resource_module = importlib.util.module_from_spec(spec)
    load_resource_module(resource_module, spec)
    add_module_to_global_modules(absolute_module_file_path, resource_module)

    return resource_module
