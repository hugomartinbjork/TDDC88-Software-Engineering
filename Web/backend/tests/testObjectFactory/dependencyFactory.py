import os
import ast
import _ast


def get_directory_class_names(directory):
    '''Getting directory class names.'''
    class_names = []
    for file in os.listdir(directory):
        if file.endswith(".py"):
            with open(os.path.join(directory, file)) as mf:
                tree = ast.parse(mf.read())
                module_classes = [_ for _ in tree.body if isinstance(
                                                    _, _ast.ClassDef)]
                module_classes = [(c.name) for c in module_classes]
                class_names.append(*module_classes)
    return (class_names)


class DependencyFactory():
    '''Dependency factory.'''
    def __init__(self) -> None:
        servicepath = os.path.abspath(os.path.join(os.path.dirname(
                                __file__), '..', '..', 'services'))
        service_class_names = get_directory_class_names(servicepath)
        service_dictionary = {}
        for service_class in service_class_names:
            service_dictionary[service_class] = random_callable

        data_access_path = os.path.abspath(os.path.join(os.path.dirname(
                                    __file__), '..', '..', 'dataAccess'))
        access_class_names = get_directory_class_names(data_access_path)
        access_dictionary = {}
        for access_class in access_class_names:
            access_dictionary[access_class] = random_callable
        self.all_dependencies = {**service_dictionary, **access_dictionary}

    def complete_dependency_dictionary(self, incomplete_dependency_dictionary):
        '''Complete dependency dictionary.'''
        temp_dictionary = self.all_dependencies.copy()
        temp_dictionary.update(incomplete_dependency_dictionary)
        return temp_dictionary


class random_callable():
    '''Mimics a dependency that is not being used.'''
    pass
