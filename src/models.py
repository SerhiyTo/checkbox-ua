from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all models in the project.
    """

    def as_dict(self):
        """
        Method to return the model as a dictionary.

        :return: the model as a dictionary.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
