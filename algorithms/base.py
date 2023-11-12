class BaseAlgorithm:
    __NAME__ = "BaseAlgorithm"
    
    def solver(self, timeout):
        raise NotImplementedError
    