codeErrors = {
    "auth": {
        "noApikeyDefined": {"code": 8001, "message": "No API KEY found on machine"},
        "noMainAccountDefined": {"code": 8010, "message": "API KEY found but no main account"},
        "apiKeyUnsecured": {"code": 8020, "message": "haapi.error.apiKeyUntrusted"},
        "warningBruteforce": {"code": 8030, "message": "haapi.error.failed"},
        "apiKeyEpired": {"code": 8040, "message": "haapi.error.apiKeyExpired"},
    },
    "cache": {"notFound": {"code": 7001, "message": "Unable to find cache"}},
    "disk": {
        "invalidPath": {"code": 9001, "message": "disk.error.invalidPath"},
        "unableToGetDriveInfo": {"code": 9002, "message": "disk.error.unableToGetDriveInfo"},
    },
    "haapi": {
        "notReachable": {"code": 1e3, "message": "haapi.error.notReachable"},
        "timeout": {"code": 1010, "message": "haapi.error.timeout"},
        "BAN": {"code": 1040, "message": "haapi.error.ban"},
        "BANCLOUDFLARE": {"code": 1041, "message": "haapi.error.banCloudflare"},
        "BLACKLIST": {"code": 1050, "message": "haapi.error.blacklist"},
        "LOCKED": {"code": 1060, "message": "haapi.error.locked"},
        "DELETED": {"code": 1070, "message": "haapi.error.deleted"},
        "RESETANKAMA": {"code": 1080, "message": "haapi.error.resetAnkama"},
        "OTPTIMEFAILED": {"code": 1090, "message": "haapi.error.otpTimeFailed"},
        "SECURITYCARD": {"code": 1100, "message": "haapi.error.securityCard"},
        "BRUTEFORCE": {"code": 1110, "message": "haapi.error.bruteForce"},
        "FAILED": {"code": 1120, "message": "haapi.error.failed"},
        "PARTNER": {"code": 1130, "message": "haapi.error.partner"},
        "MAILNOVALID": {"code": 1140, "message": "haapi.error.invalidEmail"},
        "BETACLOSED": {"code": 1150, "message": "haapi.error.closedBeta"},
        "NOACCOUNT": {"code": 1160, "message": "haapi.error.notFound"},
        "ACCOUNT_LINKED": {"code": 1170, "message": "haapi.error.linkedAccount"},
        "ACCOUNT_INVALID": {"code": 1180, "message": "haapi.error.invalidAccount"},
        "ACCOUNT_SHIELDED": {"code": 1190, "message": "haapi.error.shieldedAccount"},
        "ACCOUNT_NO_CERTIFY": {"code": 1200, "message": "haapi.error.notCertifiedAccount"},
        "ANONYMOUS_IP_FORBIDDEN": {"code": 1210, "message": "haapi.error.forbiddenIp"},
        "API_NOT_FOUND": {"code": 1220, "message": "Error from haapi: Requested API call does not exist"},
        "CODEBADCODE": {"code": 1230, "message": "haapi.error.shieldCodeIncorrect"},
        "CODEEXPIRE": {"code": 1231, "message": "haapi.error.shieldCodeExpired"},
        "CODENOTFOUND": {"code": 1232, "message": "haapi.error.shieldCodeIncorrect"},
        "kardConsumeByCode": {
            "invalid": {"code": 1240, "message": "haapi.error.kardConsumeByCode.invalid"},
            "alreadyUsed": {"code": 1241, "message": "haapi.error.kardConsumeByCode.alreadyUsed"},
            "giveToAFriend": {"code": 1242, "message": "haapi.error.kardConsumeByCode.giveToAFriend"},
        },
        "kardConsumeById": {"code": 1250, "message": "haapi.error.kardConsumeById"},
        "twitch": {
            "ConsumeEntitlement": {"code": 12610, "message": "haapi.error.twitch.ConsumeEntitlement"},
            "availableEntitlements": {
                "error": {"code": 12620, "message": "haapi.error.twitch.availableEntitlements.error"},
                "notLinked": {"code": 12621, "message": "haapi.error.twitch.availableEntitlements.notLinked"},
            },
        },
        "ACCOUNTNOCERTIFIEDGSM": {"code": 1300, "message": "haapi.error.accountNoCertifiedGSM"},
        "ACCOUNTGSMNOPROVIDER": {"code": 1301, "message": "haapi.error.accountGsmNoProvider"},
    },
    "scriptSpawn": {"unableToSpawnScript": {"code": 1e4, "message": "scriptSpawn.error.unableToSpawnScript"}},
    "release": {
        "cannotCreateTmpFolder": {"code": 5021, "message": "release.error.cannotCreateTmpFolder"},
        "cannotGetInstallInformation": {"code": 12e3, "message": "release.error.cannotGetInstallInformation"},
        "cannotUninstallWhileRunning": {"code": 5006, "message": "release.error.cannotUninstallWhileRunning"},
        "cannotInstallInFolderOfAnotherGame": {
            "code": 5010,
            "message": "release.error.cannotInstallInFolderOfAnotherGame",
        },
        "cannotInstallInNonExistingFolder": {
            "code": 5020,
            "message": "release.error.cannotInstallInNonExistingFolder",
        },
        "cannotInstallLocationIsNotAFolder": {
            "code": 5030,
            "message": "release.error.cannotInstallLocationIsNotAFolder",
        },
        "cannotInstallInANonEmptyFolder": {"code": 5040, "message": "release.error.cannotInstallInANonEmptyFolder"},
        "cannotInstallReadWritePermissions": {
            "code": 5060,
            "message": "release.error.cannotInstallReadWritePermissions",
        },
        "NOT_INSTALLED": {"code": 5e3, "message": "release.error.cannotStartNotInstalled"},
        "UPDATE_RUNNING": {"code": 5002, "message": "release.error.cannotStartWhileUpdating"},
        "UPDATE_AVAILABLE": {"code": 5003, "message": "release.error.cannotStartUpdateAvailable"},
        "MAX_RUNNING_INSTANCES_REACHED": {"code": 5011, "message": "release.error.cannotStartMaxInstancesReached"},
        "IS_MOVING": {"code": 5016, "message": "release.error.cannotStartReleaseIsMoving"},
        "SAME_FOLDER": {"code": 5017, "message": "release.error.cannotMoveSameFolder"},
        "IS_RUNNING": {"code": 5005, "message": "release.error.cannotMoveWhileRunning"},
        "USER_PERMISSIONS": {"code": 5015, "message": "release.error.cannotMoveReadWritePermissions"},
        "TEASING": {"code": 5033, "message": "release.error.cannotStartTeasing"},
    },
    "vod": {
        "apiEndpointNotFound": {"code": 6100, "message": "Requested VOD API call does not exist"},
        "underMaintenance": {"code": 6200, "message": "video.error.inMaintenance"},
        "generationTokenFailed": {"code": 6300, "message": "Generation of VOD token failed"},
        "UnableToGetSeriesList": {"code": 6400, "message": "VOD Unable to get series list"},
        "UnableToGetSeriesListWithHistory": {"code": 6500, "message": "VOD Unable to get series list with history"},
        "UnableToGetUserHistory": {"code": 6600, "message": "VOD Unable to get user history"},
        "UnableToDeleteHistory": {"code": 6700, "message": "video.error.deleteHistoryFail"},
        "NotFound": {"code": 6404, "message": "video.error.notFound"},
    },
    "universe": {
        "noUniverseAvailable": {"code": 55001, "message": "universe.errors.noUniverseAvailable"},
        "downloadMaxRetry": {"code": 55201, "message": "universe.errors.downloadMaxRetry"},
        "serviceConfigError": {"code": 55301, "message": "universe.errors.serviceConfigError"},
        "serviceNotFound": {"code": 55304, "message": "universe.errors.serviceNotFound"},
        "notFound": {"code": 55404, "message": "universe.errors.notFound"},
    },
    "sdk": {
        "axios": {
            "interceptorRequest": {"code": 10010, "message": "Something went wrong when intercepting request"},
            "interceptorFulfilledResponse": {
                "code": 10012,
                "message": "Something went wrong when intercepting fulfilled response",
            },
            "interceptorRejectedResponse": {
                "code": 10013,
                "message": "Something went wrong when intercepting rejected response",
            },
        },
        "getConfigurationInstance": {"code": 10001, "message": "Could not get configuration instance"},
        "getClassInstance": {"code": 10002, "message": "Could not get class instance"},
        "fetch": {"code": 10003, "message": "Could not fetch data"},
    },
    "tower": {
        "generationTokenFailed": {"code": 7998, "message": "Generation of Tower token failed"},
        "unsetTokenFailed": {"code": 7999, "message": "Unset Tower token failed"},
        "series": {
            "getSeriesList": {"code": 7100, "message": "Unable to get list series"},
            "getSeriesNewEpisodesList": {"code": 7101, "message": "Unable to get series new episodes list"},
            "getSeries": {"code": 7102, "message": "Unable to get series details"},
            "followSeries": {"code": 7103, "message": "Unable to follow series"},
        },
        "episode": {
            "getEpisode": {"code": 7200, "message": "Unable to get episode infos"},
            "togglelike": {"code": 7201, "message": "Unable to toggle like episode"},
            "toggleWishList": {"code": 7202, "message": "Unable to set episode to wishlist"},
            "unlockEpisodes": {"code": 7203, "message": "Unable to unlock episodes"},
            "removeFromHistory": {"code": 7204, "message": "Unable to remove episode from history"},
            "getEpisodesFromSeries": {"code": 7205, "message": "Unable to get episodes from a series"},
            "getEpisodesFromFollowedSeries": {"code": 7206, "message": "Unable to get episodes from followed series"},
        },
        "user": {
            "getFollowedSeries": {"code": 7300, "message": "Unable to get followed series"},
            "getLikedEpisodes": {"code": 7301, "message": "Unable to get liked episodes"},
            "getSeriesReadingHistory": {"code": 7302, "message": "Unable to get series reading history"},
            "getWishlist": {"code": 7303, "message": "Unable to get episodes wishlist"},
            "getRecommendations": {"code": 7304, "message": "Unable to get user series recommendations"},
            "getUnlockedEpisodes": {"code": 7305, "message": "Unable to get user unlocked episodes"},
        },
        "session": {
            "getSessionId": {"code": 7400, "message": "Unable to get session id"},
            "getReadingSessionId": {"code": 7401, "message": "Unable to get reading session id"},
            "addReadingDetails": {"code": 7402, "message": "Unable to add reading details"},
        },
        "stock": {"getWebtoonToken": {"code": 7500, "message": "Unable to get user webtoon tokens"}},
        "api": {"setAccessToken": {"code": 7600, "message": "Could not set access token"}},
        "comment": {
            "getComments": {"code": 7700, "message": "Unable to get comments"},
            "getChildComments": {"code": 7701, "message": "Unable to get child comments"},
            "createComment": {"code": 7702, "message": "Unable to create comment"},
            "updateComment": {"code": 7703, "message": "Unable to update comment"},
            "deleteComment": {"code": 7704, "message": "Unable to delete comment"},
            "replyToComment": {"code": 7705, "message": "Unable to reply to comment"},
            "reportComment": {"code": 7706, "message": "Unable to report comment"},
            "reactComment": {"code": 7707, "message": "Unable to react comment"},
        },
    },
}


def fill_rec(dict):
    result = {}
    for key in dict.keys():
        if "code" in dict[key]:
            result[dict[key]["code"]] = {"message": dict[key]["message"]}
        else:
            result.update(fill_rec(dict[key]))
    return result


MAP_CODE_TO_ERR = fill_rec(codeErrors)


def getByErrorCode(errCode):
    return MAP_CODE_TO_ERR.get(errCode)
