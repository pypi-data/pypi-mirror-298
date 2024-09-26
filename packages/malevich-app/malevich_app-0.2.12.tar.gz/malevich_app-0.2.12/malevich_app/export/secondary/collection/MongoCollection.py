from malevich_app.export.secondary.collection.Collection import Collection


class MongoCollection(Collection):
    def __init__(self, collection_id: str, mode: str = "not_check"):
        self.__collection_id = collection_id
        self.__mode = mode

    def get(self):
        return self.__collection_id

    def get_mode(self) -> str:
        return self.__mode
