# Copyright (c) PagerDuty.
# See LICENSE for details.
import six 

from .entity import Entity
from .service import Service

class Extension(Entity):
    """PagerDuty extension entity."""

    STR_OUTPUT_FIELDS = ('id', 'name',)

    ALLOWED_SERVICE_TYPES = [
        'service',
        'service_reference',
    ]

    @classmethod
    def validate(cls, service):
        """Validate `service_info` to be acceptable service data."""
        assert (service['type'] in cls.ALLOWED_SERVICE_TYPES)

    def add_service(self, service, **kwargs):
        """Add service to this extension."""
        if service is not None:
            self.__class__.validate(service)
            
        endpoint = '{0}/{1}'.format(
            self.endpoint,
            self['id']
        )

        data = self.json
        
        # apparently you can't have more than one extension?
        # BadRequest: BadRequest (2001): Invalid Input Provided - Only one extension object allowed
        data['extension_objects'] = service.json

        result = self.request('PUT', endpoint=endpoint, data=data, query_params=kwargs)
        return result

    def services(self, **kwargs):
        """Retrieve all this extensions services."""
        ids = [ref['id'] for ref in self['extension_objects']]
        return [Service.fetch(id, service=self, query_params=kwargs) for id in ids]

    def get_service(self, id, **kwargs):
        """Retrieve a single service by id."""
        return Service.fetch(id, service=self, query_params=kwargs)