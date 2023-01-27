import pathlib

class settings:

    def __init__(self, dest: pathlib.Path):
        """
        Settings for retrieving WHO speeches

        Parameters
        ----------
        dest : pathlib.Path
            The location of the retrieved speeches.
        """
        self._dest = dest

    @property
    def dest(self) -> pathlib.Path:
        return self._dest
    @property
    def metadata_json(self) -> pathlib.Path:
        return self._dest.joinpath('metadata_json')
    @property
    def speeches_html(self) -> pathlib.Path:
        return self._dest.joinpath('speeches_html')
    @property
    def speeches_txt(self) -> pathlib.Path:
        return self._dest.joinpath('speeches_txt')

    def validate(self) -> None:
        """
        Ensures the settings have face validity
        """
        def _folder(path: pathlib.Path) -> None:
            if path.exists() and not path.is_dir():
                raise ValueError(f'{str(path)} exists, but is not a folder')
        _folder(self.dest)

    def init(self) -> None:
        self.dest.mkdir(parents = True, exist_ok = True)
        self.metadata_json.mkdir(parents = True, exist_ok = True)
        self.speeches_html.mkdir(parents = True, exist_ok = True)
        self.speeches_txt.mkdir(parents = True, exist_ok = True)
