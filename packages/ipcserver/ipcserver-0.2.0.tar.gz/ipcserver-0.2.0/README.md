# ipcserver

A fastapi-like but a sock server

## Installation

```bash
pip install ipcserver
```

## Usage

```python
from ipcserver import IPCServer, IPCResponse, IpcRequest
import asyncio


app = IPCServer()


@app.route('/hello')
async def hello(request: "IpcRequest") -> "IPCResponse": # `async`, return IPCResponse and typing is required
    return IPCResponse.ok('Hello World')

if __name__ == '__main__':
    asyncio.run(app.run())
```

## Test

```python
from ipcserver import *

app = IpcServer()
def demo():
    v = APIRouter("/")

    @v.route("/")
    async def run(request: IpcRequest) -> IpcResponse:
        return IpcResponse.ok("ok")

    return v

app.include_router(demo())

@ipctest
def test01():
    client = TestClient(app)
    r = await client.send("/demo/")
    assert r.is_normal() == True
```
