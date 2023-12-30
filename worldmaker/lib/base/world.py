class World(object):
    def __init__(self,name,distribution,size) -> None:
        self.name=name
        self.distribution=distribution
        self.size=size
    def export_info_dict(self):
        return dict(name=self.name,distribution=self.distribution,size=self.size)
    def __repr__(self) -> str:
        return f"This world named '{self.name}',here some information about it:\n{self.distribution}"