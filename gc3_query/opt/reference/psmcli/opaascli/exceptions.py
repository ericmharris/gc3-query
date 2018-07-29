# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# A generic class where all the exception types are documented.
# created by sahit.gollapudi
try:
    from messages import Messages, ErrorMessages
except:
    from .messages import Messages, ErrorMessages

class OPCError(Exception):

    errMsg = 'An unspecified error occurred.'

    def __init__(self, **args):
        msg = self.errMsg.format(**args)
        Exception.__init__(self, msg)

class ResponseNullError(OPCError):

    errMsg = 'Error while trying to attempt an HTTP call.'

class UnknownArgumentError(OPCError):
    # this is called when an unknown argument is specified in the cmd line.
    errMsg = "Unknown argument {arguments}. Please execute '{cmd_struct} h' for allowed arguments."

class DataNotFoundError(OPCError):
    # if data not found in the cloud.
    errMsg = "No data found."

class OpaasConfigError(OPCError):
    # if any data is missing in the atoml file.
    errMsg = "Please configure the psm client using the command 'psm setup'."

class OpaasDownloadFileError(OPCError):
    # if the downloaded file is None.
    errMsg = "Error while trying to Download the latest version."

class PSMUsageError(OPCError):
    # display error by custom validation of arguments
    errMsg = "{usage}\n{prog}: error: {err_msg}"

class OSSUploadError(OPCError):
    # raise this exception on any error while uploading to storage cloud.
    errMsg = "Error uploading the archive to Oracle Storage Cloud. Status code {http_code}: {err_msg}"

class OSSDetailsError(OPCError):
    # raise this exception on any error while tryifn to get details from OSS
    errMsg = "Unable to get Oracle Storage Cloud details. Contact Oracle Support Services..."

class PSMOAuthError(OPCError):
    # raise this exception on any error while trying to get the access token for OAuth
    errMsg = ErrorMessages.OPAAS_CLI_GENERIC_ERR_DISPLAY

class WCJobPollingError(OPCError):
    # raise this exception on any error while trying to poll the job status for '-wc'
    errMsg = ErrorMessages.OPAAS_CLI_WC_JOB_POLLING_ERROR

class AccsStreamLogError(OPCError):
    # raise this exception while tryiing to stream log.
    errMsg = ErrorMessages.OPAAS_CLI_ACCS_STREAM_LOG_ERROR
