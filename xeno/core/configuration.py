# System imports
from sys import exit
from os.path import join, expanduser, exists, isfile
from ConfigParser import SafeConfigParser

# xeno imports
from .output import print_warning, print_error


# Global variables to track configuration
_CONFIGURATION = None


def configuration_file_path(check=True):
    """Returns the configuration file path for xeno.

    This method will compute the configuration file path and, if requested,
    validate that the path exists and that it is a file (or at least a symlink
    to a file).  If the check fails, this method will print an error and exit.

    Args:
        check: Whether or not to validate the configuration file path

    Returns:
        A string representing the configuration file path.
    """
    # Compute the path
    config_file_path = join(expanduser('~'), '.xenoconfig')

    # Do basic validation on the config file path
    if check and exists(config_file_path) and not isfile(config_file_path):
        print_error(
            'Configuration path ({0}) exists but is not a file'.format(
                config_file_path
            )
        )
        exit(1)

    return config_file_path


def get_configuration():
    """Loads the xeno configuration object.

    This method loads a ConfigParser.SafeConfigParser from the configuration
    path.  If the configuration path does not exist, this method returns an
    empty SafeConfigParser.  If called multiple times, this method returns the
    same object, so as to avoid multiple trips to disk and multiple
    inconsistent configuration objects in memory.

    Returns:
        An initialized (but possibly empty) ConfigParser.SafeConfigParser.
    """
    # Check if we have a version loaded already
    global _CONFIGURATION
    if _CONFIGURATION is not None:
        return _CONFIGURATION

    # Grab the configuration file path
    config_file_path = configuration_file_path()

    # Create a configuration parser
    _CONFIGURATION = SafeConfigParser()

    # Try to read in any existing configuration
    try:
        _CONFIGURATION.read(config_file_path)
    except Exception, e:
        print_error(
            'Unable to read configuration file ({0}): {1}'.format(
                config_file_path,
                str(e)
            )
        )
        exit(1)

    return _CONFIGURATION


def save_configuration():
    """Saves the configuration to the configuration file path.

    This method will use the current configuration (as returned from
    get_configuration) and save it to the xeno configuration file path, or if
    it is unable to do so, will print an error and exit.

    Args:
        config: A ConfigParser.SafeConfigParser representing the configuration
            to save
    """
    # Grab the configuration
    configuration = get_configuration()

    # Grab the configuration file path
    config_file_path = configuration_file_path()

    # Try to save it
    try:
        with open(config_file_path, 'w') as config_file:
            configuration.write(config_file)
    except Exception, e:
        print_error(
            'Unable to save configuration to {0}: {1}'.format(
                config_file_path,
                str(e)
            )
        )
        exit(1)
