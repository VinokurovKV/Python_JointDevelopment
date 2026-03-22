import sys
import cmd
import socket
import threading
import readline


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])


class CowClient(cmd.Cmd):
    prompt = "> "

    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def do_who(self, arg):
        self.sock.sendall(b"who\n")

    def do_cows(self, arg):
        self.sock.sendall(b"cows\n")

    def do_login(self, arg):
        self.sock.sendall(f"login {arg}\n".encode())

    def do_say(self, arg):
        self.sock.sendall(f"say {arg}\n".encode())

    def do_yield(self, arg):
        self.sock.sendall(f"yield {arg}\n".encode())

    def do_quit(self, arg):
        self.sock.sendall(b"quit\n")
        return True

    def default(self, arg):
        print("Unknown command")


def spam(cmdline, sock):
    while msg := sock.recv(1024):
        print(f"\n{msg.rstrip().decode()}\n{cmdline.prompt}{readline.get_line_buffer()}",
              end="", flush=True)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cmdline = CowClient(s)
    timer = threading.Thread(target=spam, args=(cmdline, s), daemon=True)
    timer.start()
    cmdline.cmdloop()