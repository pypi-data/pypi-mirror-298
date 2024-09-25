"""Contains the DeviceInfo class."""
import _tanway

class DeviceInfo:

    def __init__(self, impl):
        """Initialize DeviceInfo wrapper.

        This constructor is only used internally, and should not be called by the end-user.

        Args:
            impl: Reference to internal/back-end instance.

        Raises:
            TypeError: If argument does not match the expected internal class.
        """
        if not isinstance(impl, _tanway.DeviceInfo):
            raise TypeError(
                "Unsupported type for argument impl. Got {}, expected {}".format(
                    type(impl), _tanway.DeviceInfo
                )
            )
        self.__impl = impl

    @property
    def head(self):
        """Get the dif head, four bytes 0xDD, 0xEE, 0x33, 0x44

        Returns:
            A positive integer
        """
        return self.__impl.head()

    @property
    def type(self):
        """Get the type of the lidar

        Returns:
            A positive integer
        """
        return self.__impl.type()
    
    @property
    def number(self):
        """Get the number of the lidar

        Returns:
            A positive integer
        """
        return self.__impl.number()
    
    @property
    def ps_version(self):
        """Get the ps version of the lidar

        Returns:
            A string version
        """
        return self.__impl.ps_version()
    
    @property
    def pl_version(self):
        """Get the pl version of the lidar

        Returns:
            A string version
        """
        return self.__impl.pl_version()

    @property
    def mode(self):
        """Get the work mode of the lidar

        Returns:
            A positive integer
        """
        return self.__impl.mode()
    
    @property
    def status(self):
        """Get the work status of the lidar

        Returns:
            A positive integer
        """
        return self.__impl.status()
    
    @property
    def private_data(self, address):
        """Get the private data of the lidar, not open for all users

        Returns:
            A byte data with the requested address from 0 to 1023

        """
        return self.__impl.private_data(address)
    