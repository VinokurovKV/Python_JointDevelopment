#!/usr/bin/env python3
import asyncio
import shlex
import cowsay

clients = {}
logged_users = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)

    clients[me] = asyncio.Queue()
    name = None

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive],
            return_when=asyncio.FIRST_COMPLETED
        )

        for q in done:
            if q is send:
                line = q.result().decode().strip()
                send = asyncio.create_task(reader.readline())

                if not line:
                    continue

                args = shlex.split(line)

                match args:
                    case ["who"]:
                        await clients[me].put(" ".join(logged_users.keys()))

                    case ["cows"]:
                        free = [cow for cow in cowsay.list_cows() if cow not in logged_users]
                        await clients[me].put(" ".join(free))

                    case ["login", cow]:
                        if name is not None:
                            await clients[me].put("You are logged in")
                        elif cow not in cowsay.list_cows():
                            await clients[me].put("No such cow")
                        elif cow in logged_users:
                            await clients[me].put("This login is occupied")
                        else:
                            name = cow
                            logged_users[name] = me
                            await clients[me].put(f"Logged in as {name}")

                    case ["say", cow, *text]:
                        if name is None:
                            await clients[me].put("Login first")
                        elif cow not in logged_users:
                            await clients[me].put("Login is not known")
                        else:
                            msg = " ".join(text)
                            target = logged_users[cow]
                            await clients[target].put(cowsay.cowsay(msg, cow=name))

                    case ["yield", *text]:
                        if name is None:
                            await clients[me].put("Login first")
                        else:
                            msg = " ".join(text)
                            out = cowsay.cowsay(msg, cow=name)
                            for user, peer in logged_users.items():
                                if peer != me:
                                    await clients[peer].put(out)

                    case ["quit"]:
                        if name is not None:
                            del logged_users[name]

                        send.cancel()
                        receive.cancel()
                        del clients[me]
                        writer.close()
                        await writer.wait_closed()
                        print(me, "DONE")
                        return

                    case _:
                        await clients[me].put("Unknown command")

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()

    if name is not None:
        del logged_users[name]

    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
