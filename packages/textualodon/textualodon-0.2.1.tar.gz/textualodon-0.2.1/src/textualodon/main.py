try:
    from .textualodon import Textualodon
except ImportError:
    from textualodon import Textualodon  # type: ignore[no-redef]


def main():
    app = Textualodon()
    app.run()


if __name__ == "__main__":
    main()
