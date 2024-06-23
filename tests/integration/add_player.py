from starlette.testclient import TestClient

from src.server import app


def test_add_player():
    client = TestClient(app=app)
    with client.websocket_connect("/holdem") as websocket:
        websocket.send_json(
            {
                "command": "add_player",
                "player": {
                    "address": "0x1",
                    "balance": 5000
                }
            }
        )
        websocket.send_json(
            {
                "command": "add_player",
                "player": {
                    "address": "0x2",
                    "balance": 5000
                }
            }
        )
        websocket.send_json(
            {
                "command": "add_player",
                "player": {
                    "address": "0x3",
                    "balance": 5000
                }
            }
        )
        websocket.send_json({"command": "start_deal"})
        response = websocket.receive_json()
        assert response["bet"] == 2
        assert response["excluded_actions"] == "check"
        assert response["player_last_bet"] == 0
        player = response["player"]
        assert player["address"] == "0x3"
        assert player["balance"] == 5000
        assert player["hand"]
        assert player["idx"] == 2
        assert player["name"] == "Player 3"
        print(player)
        player["action"] = "call"
        websocket.send_json(
            {"command": "make_move", "player": player}
        )
        response = websocket.receive_json()
        assert response["bet"] == 2
        assert response["excluded_actions"] == "check"
        assert response["player_last_bet"] == 1
        player = response["player"]
        assert player["address"] == "0x1"
        assert player["balance"] == 4999
        assert player["hand"]
        assert player["idx"] == 0
        assert player["name"] == "Player 1"
