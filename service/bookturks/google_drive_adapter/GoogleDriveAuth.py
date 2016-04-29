import argparse
import httplib2
from googleapiclient import discovery

from oauth2client import client
from oauth2client import file
from oauth2client import tools


def get_credentials(client_secrets_path, doc="", argv=None, name='storage', version='v3', scope_param=None,
                    parents=[],
                    discovery_filename=None):
    """
    Args:
      argv: list of string, the command-line parameters of the application.
      name: string, name of the API.
      version: string, version of the API.
      doc: string, description of the application. Usually set to __doc__.
      client_secrets_path: string, filename of the application. Usually set to __file__.
      parents: list of argparse.ArgumentParser, additional command-line flags.
      scope_param: string, The OAuth scope used.
      discovery_filename: string, name of local discovery file (JSON). Use when discovery doc not available via URL.

    Returns:
      A tuple of (service, flags), where service is the service object and flags
      is the parsed command-line flags.
    """
    if scope_param is not None:
        scope = 'https://www.googleapis.com/auth/' + scope_param
    else:
        scope = 'https://www.googleapis.com/auth/'

    # Parser command-line arguments.
    if argv:
        parent_parsers = [tools.argparser]
        parent_parsers.extend(parents)
        parser = argparse.ArgumentParser(
            description=doc,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=parent_parsers)
        flags = parser.parse_args(argv[1:])
    else:
        flags = None

    # Name of a file containing the OAuth 2.0 information for this
    # application, including client_id and client_secret, which are found
    # on the API Access tab on the Google APIs
    # Console <http://code.google.com/apis/console>.
    client_secrets = client_secrets_path

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(client_secrets,
                                          scope=scope,
                                          message=tools.message_if_missing(client_secrets),
                                          redirect_uri="http://bookturks.herokuapp.com")

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(name + '.json')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secrets, scope, redirect_uri="http://bookturks.herokuapp.com")
        credentials = tools.run_flow(flow, storage, flags) \
            if flags else tools.run_flow(flow, storage, tools.argparser.parse_args([]))
    http = credentials.authorize(http=httplib2.Http())

    if discovery_filename is None:
        # Construct a service object via the discovery service.
        service = discovery.build(scope_param, version, http=http)
    else:
        # Construct a service object using a local discovery document file.
        with open(discovery_filename) as discovery_file:
            service = discovery.build_from_document(
                discovery_file.read(),
                base='https://www.googleapis.com/',
                http=http)
    return service
