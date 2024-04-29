
import connect
from abc import ABC, abstractmethod
from models import Quotes, Authors, Tag


class DataProvider(ABC):
    def __init__(self) -> None:
        ...

    @abstractmethod
    def query_author_by_name(self, name: str):
        ...

    @abstractmethod
    def query_quotes_by_author(self, author) -> list[str]:
        ...

    @abstractmethod
    def query_quotes_by_tags(self, tags: list[str]) -> list[str]:
        ...


class MongoDataProvider(DataProvider):
    def __init__(self) -> None:
        ...

    def query_author_by_name(self, name: str) -> Authors:
        author = Authors.objects(fullname__istartswith=name).first()
        return author

    def query_quotes_by_author(self, author: Authors) -> list[str]:
        try:
            quotes = Quotes.objects(author=author.id)
            return self.__format_quotes(quotes)
        except AttributeError:
            return None

    def query_quotes_by_tags(self, tags: list[str]) -> list[str]:
        quotes = Quotes.objects(tags__name__in=tags)
        return self.__format_quotes(quotes)
    
    def __format_quotes(self, quotes: Quotes) -> list[str]:
        result = []
        for quote in quotes:
            result.append(f"{quote.quote}")
        return result


class Cache(ABC):
    def __init__(self) -> None:
        ...

    @abstractmethod
    def get_cache_record(self, key: str) -> str:
        ...
    
    @abstractmethod
    def set_cache_record(self, key: str, value: str) -> None:
        ...

    def get_cache_key(self, prefix: str, suffix: str) -> str:
        return f"{prefix}:{suffix}"


class RedisCache(Cache):
    def __init__(self) -> None:
        ...

    def get_cache_record(self, key: str) -> str:
        ...
    
    def set_cache_record(self, key: str, value: str) -> None:
        ...


class DataManager():
    def __init__(self, cache: Cache, data_provider: DataProvider) -> None:
        self.__cache: Cache = cache
        self.__data_provider: DataProvider = data_provider

    def query_by_author(self, name: str) -> list[str]:
        cache_key = self.__cache.get_cache_key("author", name) # "author:steve martin"
        result = self.__cache.get_cache_record(cache_key)
        if result: 
            return result
        author = self.__data_provider.query_author_by_name(name)
        if author:
            result = self.__data_provider.query_quotes_by_author(author)
            if result:
                self.__cache.set_cache_record(cache_key, result)
        else: 
            result = [f"Author with name '{name.title()}' not found"]        
        return result or ["No results found"]


    def query_by_tags(self, tags: list[str]) -> str:
        cache_key = self.__cache.get_cache_key("tags", ",".join(tags)) # "tags:live,life"
        result = self.__cache.get_cache_record(cache_key)
        if result: 
            return result
        result = self.__data_provider.query_quotes_by_tags(tags)
        if result:
            self.__cache.set_cache_record(cache_key, result)
        return result or ["No results found"]


class CommandManager:
    def __init__(self, data_manager: DataManager) -> None:
        self._exit_commands = {"good bye", "close", "exit", "stop", "g"}
        self._commands = {"name": self.get_quotes_by_author, "tag": self.get_quotes_by_tags, "tags": self.get_quotes_by_tags}
        self._data_manager = data_manager

    def is_exit(self, user_input) -> bool:
        return user_input in self._exit_commands

    def handle_command(self, user_input: str) -> str:
        args = user_input.lower().split(":")
        try:
            return self._commands[args[0]](args[1].strip())
        except KeyError:
            return "Unknown command"
        except IndexError:
            return "Wrong command format"

    def get_quotes_by_author(self, name: str) -> str:
        return self._data_manager.query_by_author(name)

    def get_quotes_by_tags(self, tags: str) -> str:
        tag_list = tags.split(",")
        return self._data_manager.query_by_tags(tag_list)


def format_output(output) -> str:
    if isinstance(output, str):
        return output
    return "\n".join(output)

def get_help() -> str:
    return """
    Supported commands:
    name: [author name] - prints quotes by author name
    tag:[tag] - prints quotes by a tag
    tags:[tag-1],[tag-2],...,[tag-n] - prints quotes by a tags
"""


def main():
    manager = CommandManager(DataManager(RedisCache(), MongoDataProvider()))
    print(get_help())
    while True:
        user_input = input(">>> ")

        if manager.is_exit(user_input):
                print("Good bye!")
                break
        
        print(format_output(manager.handle_command(user_input)))


if __name__ == '__main__':
    main()















# from models import Notes
# import connect


# print('--- All notes ---')
# notes = Notes.objects()
# for note in notes:
#     records = [f'description: {record.description}, done: {record.done}' for record in note.records]
#     tags = [tag.name for tag in note.tags]
#     print(f"id: {note.id} name: {note.name} date: {note.created} records: {records} tags: {tags}")

# print('--- Notes with tag Fun ---')

# notes = Notes.objects(tags__name='Fun')
# for note in notes:
#     records = [f'description: {record.description}, done: {record.done}' for record in note.records]
#     tags = [tag.name for tag in note.tags]
#     print(f"id: {note.id} name: {note.name} date: {note.created} records: {records} tags: {tags}")

# print('--- Notes with tags Fun and Purchases ---')

# notes = Notes.objects(tags__name__in=['Fun', 'Purchases'])
# for note in notes:
#     records = [f'description: {record.description}, done: {record.done}' for record in note.records]
#     tags = [tag.name for tag in note.tags]
#     print(f"id: {note.id} name: {note.name} date: {note.created} records: {records} tags: {tags}")

# Оновлення 

# _id = '662d01f45f29a385de55da60'
# note = Notes.objects(id=_id)
# note.update(name='New Shopping') 

# Bидалення даних

# _id = '662d01f45f29a385de55da60'
# note = Notes.objects(id=_id).delete()
