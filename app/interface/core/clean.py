from docker.errors import APIError
from django.conf import settings

from systems.command.types import environment

import re


class Command(environment.EnvironmentActionCommand):

    def exec(self):
        base_image = re.sub(r'\:.+$', '', settings.DEFAULT_RUNTIME_IMAGE)
        images = []

        for image in self.manager.client.images.list():
            if re.match(rf"^{base_image}\:[\d]+$", image.tags[0]):
                images.append(image)

        def remove(image):
            try:
                self.manager.client.images.remove(image.id)
                self.success("Successfully removed image: {}".format(image.tags[0]))

            except APIError as e:
                if e.response.status_code != 409:
                    raise e

        self.run_list(images, remove)
