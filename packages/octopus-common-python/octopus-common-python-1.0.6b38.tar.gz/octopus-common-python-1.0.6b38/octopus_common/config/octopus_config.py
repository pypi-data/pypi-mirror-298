from octopus_common.constant.constants import WORKING_DIRECTOR
from octopus_common.util.file_utils import read_properties

LOCAL_AUTH_CONFIG = read_properties(WORKING_DIRECTOR + '/Auth.properties')
LOCAL_CLIENT_CONFIG = read_properties(WORKING_DIRECTOR + '/client.properties')
