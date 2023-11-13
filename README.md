### Learning HFT LLD - Zerodha

Simulating Zerodha's trading algo in FastAPI Python while going through @hkirat YT tutorial

Initial user Balances with market ticker set only as 'GOOGLE' for simplicity

```python

users: List[User] = [
    {
        "id": "1",
        "balances": {
            "GOOGLE": 10,
            "USD": 50000,
        }
    },
    {
        "id": "2",
        "balances": {
            "GOOGLE": 10,
            "USD": 50000,
        }
    }
]
```

To run and check the correctness of the simulated algo:

Testing by calling endpoints, run the uvicorn server for that:

```
uvicorn main:app --reload

```

Then call the endpoints through Postman, Curl or using python requests

or run the pytest present in the test_main.py file:

```
pytest

```

All 6 tests should pass
