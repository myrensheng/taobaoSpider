class SessionException(Exception):
    """
    会话异常
    """
    def __init__(self,message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message
