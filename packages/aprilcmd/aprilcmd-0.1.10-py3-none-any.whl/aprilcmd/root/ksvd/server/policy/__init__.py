
class PolicyManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "policy"
        self.type = "Policys"
        pass

    def check(self):
        return False

manager = PolicyManger()