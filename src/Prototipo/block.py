
class Block:
    def __init__(self, bd, limit, pid):
        self._bd = bd
        self._limit = limit
        self._moreSpace = 0
        self._pid = pid

    def get_Bd(self):
        return self._bd

    def get_Limit(self):
        return self._limit

    def get_Pid(self):
        return self._pid

    def get_Size(self):
        return self._limit - self._bd + 1 - self._moreSpace


    def set_bd(self, bd):
        self._bd = bd

    def set_limit(self, limit):
        self._limit = limit

    def set_pid(self, pid):
        self._pid = pid

    def set_moreSpace(self, moreSpace):
        self._moreSpace = moreSpace

    def get_moreSpace(self):
        return self._moreSpace

    def __repr__(self):
        if self._moreSpace != 0:
            return "Bd={bd:2d}  Limit={limit:2d}  Size={size:2d}  Pid={pid:2d}  Ms={ms}".format(bd=self._bd, limit=self._limit, size=self.get_Size(), pid=self._pid, ms=self._moreSpace)
        else:
            return "Bd={bd:2d}  Limit={limit:2d}  Size={size:2d}  Pid={pid:2d}".format(bd=self._bd, limit=self._limit, size=self.get_Size(), pid=self._pid)


