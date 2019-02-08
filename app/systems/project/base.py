from django.conf import settings

from systems.command import providers

import os
import re
import pathlib
import yaml


class BaseProjectProvider(providers.DataCommandProvider):

    def __init__(self, name, command, instance = None):
        super().__init__(name, command, instance)
        self.provider_type = 'project'
        self.provider_options = { k: v for k, v in settings.PROJECT_PROVIDERS.items() if k != 'internal' }


    @property
    def facade(self):
        return self.command._project


    def create(self, name, fields):
        fields['type'] = self.name
        return super().create(name, fields)
    

    def project_path(self, name):
        env = self.command.curr_env
        path = os.path.join(settings.PROJECT_BASE_PATH, env.name, name)
        pathlib.Path(path).mkdir(parents = True, exist_ok = True)
        return path


    def get_task(self, task_name):
        config = self.load_yaml('cenv.yml')
        
        if task_name not in config:
            self.command.error("Task {} not found in project {} cenv.yml".format(task_name, self.instance.name))
        
        task = config[task_name]
        provider = task.pop('provider')

        return self.command.get_provider(
            'task', provider, self, task
        )

    def exec(self, task_name, servers, params = {}):
        instance = self.check_instance('project exec')
        task = self.get_task(task_name)
        
        if task.check_access():
            self.install_requirements(task.get_requirements())
            task.exec(servers, params)
        else:
            self.command.error("Access is denied for task {}".format(task_name))


    def load_file(self, file_name, binary = False):
        instance = self.check_instance('project load file')
        project_path = self.project_path(instance.name)
        path = os.path.join(project_path, file_name)
        operation = 'rb' if binary else 'r'
        content = None

        if os.path.exists(path):
            with open(path, operation) as file:
                content = file.read()
        
        return content

    def load_yaml(self, file_name):
        return yaml.load(self.load_file(file_name))


    def save_file(self, file_name, content = '', binary = False):
        instance = self.check_instance('project save file')
        project_path = self.project_path(instance.name)
        path = os.path.join(project_path, file_name)
        operation = 'wb' if binary else 'w'
        
        pathlib.Path(path).mkdir(parents = True, exist_ok = True)

        with open(path, operation) as file:
            file.write(content)
        
        return content

    def save_yaml(self, file_name, data = {}):
        return self.save_file(file_name, yaml.dump(data))


    def install_requirements(self, requirements = []):
        overrides = self.parse_requirements('requirements.txt')
        req_map = {}

        if len(overrides):
            requirements.extend(overrides)    

        for req in requirements:
            # PEP 508
            req_map[re.split(r'[\>\<\!\=\~\s]+', req)[0]] = req

        requirements = list(req_map.values())

        if len(requirements):
            success, stdout, stderr = self.command.sh(['pip3', 'install'] + requirements)
        
            if not success:
                self.command.error("Installation of requirements failed: {}".format("\n".join(requirements)))

    def parse_requirements(self, file_name):
        requirements = []
        file_contents = self.load_file(file_name)

        if file_contents:
            requirements = [ req for req in file_contents.split("\n") if req and req[0].strip() != '#' ]
        
        return requirements
