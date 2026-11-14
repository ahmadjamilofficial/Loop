<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from loop import Loop


with Loop() as l_client:

    res = l_client.health.health()

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from loop import Loop

async def main():

    async with Loop() as l_client:

        res = await l_client.health.health_async()

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->