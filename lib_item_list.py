from dataclasses import dataclass, field, fields
from typing import List, Any
from operator import attrgetter


@dataclass
class Item:
    def get_attr_names(self) -> list:
        return [attr_name for attr_name in fields(self)]

    def get_value(self, attribute) -> Any:
        return getattr(self, attribute)

    def __repr__(self) -> str:
        return ";".join(str(item) for item in self.__iter__())

    def __iter__(self) -> list:
        return [self.get_value(attr_name) for attr_name in self.get_attr_names()]


@dataclass(order=True)
class ItemList:
    item_list: List[Item] = field(default_factory=list)

    def __repr__(self) -> str:
        return "\n".join(str(item) for item in self.item_list)

    def __iter__(self) -> list:
        return [item for item in self.item_list]

    def __getitem__(self, index: int) -> Item:
        return self.item_list[index]

    def __len__(self) -> int:
        return len(self.item_list)

    def clear(self) -> None:
        self.item_list.clear()

    def add_item(self, data: Item) -> None:
        self.item_list.append(data)

    def sort_list(self, attribute: Any, desc: bool = False):
        if isinstance(attribute, str):
            self.item_list.sort(key=attrgetter(attribute), reverse=desc)
        else:
            self.item_list.sort(key=attrgetter(*attribute), reverse=desc)
        return self

    def get_header(self) -> list:
        return [self.item_list[0].get_attr_names()]

    def get_list(self) -> list:
        return [list(item) for item in self.item_list]

    def get_column(self, column: str) -> list:
        return [item.get_value(column) for item in self.item_list]
