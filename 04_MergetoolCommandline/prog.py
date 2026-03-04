import cmd
import shlex
import cowsay

def side_by_side(left, right):
    l = left.splitlines()
    r = right.splitlines()

    lw = max(map(len, l)) if l else 0
    rw = max(map(len, r)) if r else 0

    if len(l) < len(r):
        l = [" " * lw] * (len(r) - len(l)) + l
    elif len(r) < len(l):
        r = [" " * rw] * (len(l) - len(r)) + r

    for a, b in zip(l, r):
        print(a.ljust(lw) + " " + b)

class twocows(cmd.Cmd):
    prompt = "twocows> "

    def do_list_cows(self, arg):
        """Listing cows"""
        if shlex.split(arg):
            return
        print(" ".join(cowsay.list_cows()))

    def do_make_bubble(self, arg):
        """Making bubble"""
        args = shlex.split(arg)
        match args:
            case [msg]:
                print(cowsay.make_bubble(msg))
            case _:
                print(" ! ")

    def do_cowsay(self, arg):
        """Speaking cows"""
        args = shlex.split(arg)
        if "reply" not in args:
            return

        i = args.index("reply")
        left = args[:i]
        right = args[i + 1 :]

        if len(left) != 1 or len(right) != 1:
            return

        out1 = cowsay.cowsay(left[0])
        out2 = cowsay.cowsay(right[0])
        side_by_side(out1, out2)

    def do_exit(self, arg):
        """exit"""
        return 1

if __name__ == "__main__":
    twocows().cmdloop()