class User:

    def __init__(self, operator, priority):
        self.operator = operator
        self.priority = priority

    def getName(self):
        return self.operator

    def higher(self, user):
        return True if self.priority > user.priority else False

    def lower(self, user):
        return not self.higher(user)
