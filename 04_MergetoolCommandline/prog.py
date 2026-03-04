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
        right = args[i + 1:]

        if len(left) < 1 or len(right) < 1:
            return

        msg1, cow1, p1 = self.parse_one(left)
        msg2, cow2, p2 = self.parse_one(right)

        if msg1 is None or msg2 is None:
            return

        out1 = cowsay.cowsay(
            msg1,
            cow=cow1,
            eyes=p1.get("eyes", "oo"),
            tongue=p1.get("tongue", "  "),
        )

        out2 = cowsay.cowsay(
            msg2,
            cow=cow2,
            eyes=p2.get("eyes", "oo"),
            tongue=p2.get("tongue", "  "),
        )

        side_by_side(out1, out2)

    def do_cowthink(self, arg):
        """Thinking cows"""
        args = shlex.split(arg)

        if "reply" not in args:
            return

        i = args.index("reply")
        left = args[:i]
        right = args[i + 1:]

        if len(left) < 1 or len(right) < 1:
            return

        msg1, cow1, p1 = self.parse_one(left)
        msg2, cow2, p2 = self.parse_one(right)

        if msg1 is None or msg2 is None:
            return

        out1 = cowsay.cowthink(
            msg1,
            cow=cow1,
            eyes=p1.get("eyes", "oo"),
            tongue=p1.get("tongue", "  "),
        )

        out2 = cowsay.cowthink(
            msg2,
            cow=cow2,
            eyes=p2.get("eyes", "oo"),
            tongue=p2.get("tongue", "  "),
        )

        side_by_side(out1, out2)

    def parse_one(self, tokens):
        msg = tokens[0]
        cow = "default"
        params = {}

        if len(tokens) >= 2:
            cow = self.resolve_cow(tokens[1])
            if cow is None:
                return None, None, None

        if len(tokens) >= 3:
            for t in tokens[2:]:
                if "=" not in t:
                    return None, None, None
                k, v = t.split("=", 1)
                if k not in ("eyes", "tongue"):
                    return None, None, None
                params[k] = v

        return msg, cow, params

    def resolve_cow(self, prefix):
        cows = cowsay.list_cows()

        if prefix in cows:
            return prefix

        matches = [c for c in cows if c.startswith(prefix)]

        if len(matches) == 1:
            return matches[0]

        return None

    def do_exit(self, arg):
        """exit"""
        return 1

if __name__ == "__main__":
    twocows().cmdloop()
