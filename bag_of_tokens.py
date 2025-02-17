"""A bag of tokens emulator."""

import random

from constants import TOKENS
from exceptions import UnexpectedToken, DontWantAddToken, EmptyBag


class Bag():
    """Bag of tokens."""

    def __init__(self):
        """Init."""
        self.token_set = []

    def get_token(self) -> None:
        """Get token from bag."""
        if self.token_set:
            return random.choice(self.token_set)
        raise EmptyBag

    def add_token_set(self, token_set: str) -> None:
        """Add token set to the bag."""
        if not isinstance(token_set, str):
            token_set = str(token_set)
        split_token_set = token_set.split(' ')
        for token in split_token_set:
            if token not in TOKENS:
                print(f'Жетона {token} не существует. Попробуйте снова. '
                      f'Список возможных жетонов: {TOKENS}')
                return
            self.token_set.append(token)
        print(f'Набор жетонов {token_set} успешно добавлен в мешок.')

    def add_token(self, new_token: str) -> None:
        """Add token to the bag."""
        if not isinstance(new_token, str):
            new_token = str(new_token)
        if new_token == 'Не хочу добавлять жетон':
            raise DontWantAddToken
        if new_token not in TOKENS:
            message = ('Такого жетона не существует. Попробуйте снова. '
                       f'Список возможных жетонов: {TOKENS}')
            raise UnexpectedToken(message)
        self.token_set.append(new_token)
        print(f'Жетон {new_token} успешно добавлен в мешок.')

    def __str__(self):
        if not self.token_set:
            return 'Мешок пуст'
        else:
            token_set = ' '.join(self.token_set)
            return f'В мешке лежат жетоны: {token_set}'

    def delete_token(self):
        pass

    def delete_all_tokens(self):
        pass


def main():
    """Main."""
    pass


if __name__ == '__main__':
    main()
