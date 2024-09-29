import asyncio

from bonchapi import BonchAPI


async def main():
    api = BonchAPI()
    
    await api.login("karimullinarthur@disroot.org", "CVBcvb2005")
    rsp = await api.get_timetable()
    for day in rsp:
        if day["date"] == "30.9.2024":
            print(day)

asyncio.run(main())
