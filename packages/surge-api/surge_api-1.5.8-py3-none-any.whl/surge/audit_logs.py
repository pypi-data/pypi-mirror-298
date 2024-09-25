import dateutil.parser

from surge.errors import SurgeMissingIDError
from surge.api_resource import AUDIT_LOGS_ENDPOINT, APIResource


class AuditLog(APIResource):

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

        if self.id is None:
            raise SurgeMissingIDError

        if self.description is None:
            self.description = ""

        if hasattr(self, "created_at") and self.created_at:
            # Convert timestamp str into datetime
            self.created_at = dateutil.parser.parse(self.created_at)

    def __str__(self):
        return f"<surge.Team#{self.id}>"

    def __repr__(self):
        return f"<surge.Team#{self.id} {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["id"])

    @classmethod
    def list(cls):
        '''
        Lists all of your teams.
        Returns:
            teams (list): list of Team objects.
        '''
        endpoint = f"{AUDIT_LOGS_ENDPOINT}/list"
        response_json = cls.get(endpoint)
        tasks = [Team(**team_data) for team_data in response_json]
        return tasks
