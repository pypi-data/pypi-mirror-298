from abc import abstractmethod
from uuid import UUID

from lqs.interface.base.delete import DeleteInterface as BaseDeleteInterface
import lqs.interface.dsm.models as models


class DeleteInterface(BaseDeleteInterface):
    @abstractmethod
    def _announcement(self, **kwargs):
        pass

    def announcement(self, announcement_id: UUID):
        return self._announcement(
            announcement_id=announcement_id,
        )

    @abstractmethod
    def _comment(self, **kwargs):
        pass

    def comment(self, comment_id: UUID):
        return self._comment(
            comment_id=comment_id,
        )

    @abstractmethod
    def _configuration(self, **kwargs):
        pass

    def configuration(self, configuration_id: UUID):
        return self._configuration(
            configuration_id=configuration_id,
        )

    @abstractmethod
    def _datastore(self, **kwargs):
        pass

    def datastore(self, datastore_id: UUID):
        return self._datastore(
            datastore_id=datastore_id,
        )

    @abstractmethod
    def _datastore_association(self, **kwargs):
        pass

    def datastore_association(self, datastore_association_id: UUID):
        return self._datastore_association(
            datastore_association_id=datastore_association_id,
        )

    @abstractmethod
    def _usage_record(self, **kwargs):
        pass

    def usage_record(self, timestamp: models.Int64, datastore_id: UUID):
        return self._usage_record(
            timestamp=timestamp,
            datastore_id=datastore_id,
        )
