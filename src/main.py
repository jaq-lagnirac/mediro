# Justin Caringal
#
# The main driver program for the Mediro application

from gui import MainWindow

def main() -> None:
    """The main function of the entire application."""
    window = MainWindow()
    window.mainloop()

if __name__ == "__main__":
    main()