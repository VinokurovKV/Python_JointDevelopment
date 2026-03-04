import cmd
import shlex
import cowsay


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

    def do_exit(self, arg):
        """exit"""
        return 1

if __name__ == "__main__":
    twocows().cmdloop()