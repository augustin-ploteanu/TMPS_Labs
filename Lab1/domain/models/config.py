class Config:
    """
    Very simple Singleton for global app configuration.
    Usage:
        c1 = Config()
        c2 = Config()
        assert c1 is c2
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # first and only time we create it
            cls._instance = super().__new__(cls)
            # you can initialize default values here
            cls._instance.env = "dev"
            cls._instance.debug = True
        return cls._instance

    def __repr__(self):
        return f"<Config env={self.env!r} debug={self.debug!r}>"
