1. Запуск сервера
Пакетный менеджер:
    https://python-poetry.org/docs/
```bash
poetry install
poetry run task dev
```
2. Формат обмена данными - JSON.
3. В модуле src.core.models.models модель запросов: 


Основная сущность, через интерфейсы которой ведется управление игрой - State. 
Инкапсулирует всю логику внутри себя: 
    сборка колоды, сдача карт 
    перестановка игроков в очереди
    вывод игроков в фолд и восстановление в очередь по окончанию раздачи 
    переключении этапов (init, flop, river, turn)
    управление ставками, блайндами и т.п.

```
class RequestModel(BaseModel):
    command: ProcedureEnum  -  команда, которая дергает метод State
    player: PayablePlayerModel | None = None  -  модель данных игрока
```
* Команды представлены Enum-ами:

```
class ProcedureEnum(str, Enum):
    JOIN: str = "add_player"  -  присоединить игрока к столу
    START: str = "start_deal" -  начать игру (внутри метода проверка, что игроков более 1-го)
    MOVE: str = "make_move" - сделать ход
    COMPLETE: str = "complete_turn" - закончить раунд 
    (под раундом понимаем круг ставок до их равенства всеми оставшимися игроками)
```

* Модель игрока:

```
class PayablePlayerModel(BaseModel):
    address: str - адрес кошелька
    hand: list[Card | None] = [] - карты игрока
    name: str | None = None - State дает дефолтное имя игроку Player<queue_idx + 1> 
    idx: int | None = None - State задает индекс игроку
    action: ActionEnum | None = None  - действие игрока (call | fold | raise | check)
    balance: int  - передаем баланс игрока при подключении игрока к игре
    amount: int | None = None  - ставка игрока (только для случая raise, для остальных случаев State сам берет нужное значение)
```

* Модель карты:

```
class SuitEnum(str, Enum): Тут может быть и нет смысла задавать масти эмодзи. Думаю, поменяем потом на ascii
    D: str = "♦"
    H: str = "♥"
    C: str = "♣"
    S: str = "♠"

class Card(BaseModel):
    suit: SuitEnum
    rank: int  - от 2 до 14
```

* Перечень действий игрока:
```
class ActionEnum(str, Enum):
    RAISE: str = "raise_"
    CALL: str = "call"
    CHECK: str = "check"
    FOLD: str = "fold"
```

* Модель ответа от сервера:
```
class Response(BaseModel):
    player: PayablePlayerModel  - неныщний игрок
    bet: int - нынещняя ставка в игре (то, что нужно поддержать, либо перебить, либо сфолдить)
    player_last_bet: int - последняя ставка данного игрока
    excluded_actions: ActionEnum | None = None - действия недоступные игроку (например, если ставка была поднята другим игроком, то игрок не может сделать check)
    
class WinnerResponse(BaseModel):
    players: list[PayablePlayerModel] - возвращает массив победителей - метод у State еще не реализован
```

4. Подключенние к сокету:

    ws://localhost:8000/holdem

    Например:
```bash
websocat ws://localhost:8000/holdem
```

5. Типичная схема взаимодействия с сервером:

* Подключение игрока
```bash
{
  "command": "add_player",
  "player": {
              "address": "0x1",
              "balance": 5000
            }
}
```

* Начало игры (должно быть не менее 2ух игроков)
```bash
{"command": "start_deal"}
```

* Ход игрока - call
```bash
{
  "command": "make_move", 
  "player": {
    "address": "0x1", 
    "hand": [
              {
                "suit": "♣", 
                "rank": 11
              }, 
              {
                "suit": "♠", 
                "rank": 8
              }
            ], 
    "name": "Player 1", 
    "idx": 0, 
    "action": "call", 
    "balance": 5000
    }
}
```

* После всего круга ставок - перевод на следующий этап
```bash
{
  "command": "complete_turn"
}
```