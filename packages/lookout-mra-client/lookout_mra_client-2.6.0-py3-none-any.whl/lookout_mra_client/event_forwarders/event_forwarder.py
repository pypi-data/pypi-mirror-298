class EventForwarder:
    """
    Generic interface for standardization of MRAv2StreamHandler
    """

    def write(self, _event: dict, _entName: str):
        raise NotImplementedError("Event forwarders must implement '.write()'")
