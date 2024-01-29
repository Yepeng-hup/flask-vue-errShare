import {post, get, del} from "./axiosPlus"


// ############################## user #####################################
export const showUserGet = data => {

    return get(
        {
            url: "/user/get",
            data
        }
    )
}

export const searchUserGet = data => {

    return get(
        {
            url: "/user/search",
            data
        }
    )
}

export const createUserPost = data => {
    return post(
        {
            url: "/user/create",
            data
        }
    )
}

export const updateUserPost = data => {
    return post(
        {
            url: "/user/update",
            data
        }
    )
}


export const delUserDelete = data => {
    return del(
        {
            url: "/user/delete",
            data
        }
    )
}


export const updateUserPwdPost = data => {
    return post(
        {
            url: "/user/update/passwd",
            data
        }
    )
}

export const getUserDataGet = data => {
    return get(
        {
            url: "/user/data/pic",
            data
        }
    )
}

export const getBlackUserDataGet = data => {
    return get(
        {
            url: "/user/blacklist",
            data
        }
    )
}

export const delBlackUserDelete = data => {
    return del(
        {
            url: "/user/blacklist/del",
            data
        }
    )
}


// ############################## Text #####################################

export const contentWritePost = data => {
    return post(
        {
            url: "/wz/w",
            data
        }
    )
}

export const searchContentPost = data => {
    return post(
        {
            url: "/wz/s",
            data
        }
    )
}

export const editContentPost = data => {
    return post(
        {
            url: "/wz/edit/show",
            data
        }
    )
}

export const updateContentPost = data => {
    return post(
        {
            url: "/wz/edit/update",
            data
        }
    )
}

export const showArticleGet = data => {
    return get(
        {
            url: "/wz/r",
            data
        }
    )
}

export const delTextDelete = data => {
    return del(
        {
            url: "/wz/d",
            data
        }
    )
}

export const addLabelPost = data => {
    return post(
        {
            url: "/wz/label/w",
            data
        }
    )
}

export const getLabelGet = data => {
    return get(
        {
            url: "/wz/label/r",
            data
        }
    )
}

export const showWzLabelGet = data => {
    return get(
        {
            url: "/wz/label/show",
            data
        }
    )
}

export const delLabelDelete = data => {
    return del(
        {
            url: "/wz/label/d",
            data
        }
    )
}


export const addClassPost = data => {
    return post(
        {
            url: "/wz/class/w",
            data
        }
    )
}

export const getClassGet = data => {
    return get(
        {
            url: "/wz/class/r",
            data
        }
    )
}

export const showWzClassGet = data => {
    return get(
        {
            url: "/wz/class/show",
            data
        }
    )
}

export const screenClassPost = data => {
    return post(
        {
            url: "/wz/class/screen",
            data
        }
    )
}

export const delClassDelete = data => {
    return del(
        {
            url: "/wz/class/d",
            data
        }
    )
}


// ###################### recovery api ######################################

export const getRecoveryInfoGet = data => {
    return get(
        {
            url: "/wz/recovery/r",
            data
        }
    )
}

export const delRecDelete = data => {
    return del(
        {
            url: "/wz/recovery/d",
            data
        }
    )
}

export const revokeRecPost = data => {
    return post(
        {
            url: "/wz/recovery/c",
            data
        }
    )
}


// ######################## home api #############################

export const getLoginInfoGet = data => {
    return get(
        {
            url: "/info/l",
            data
        }
    )
}

export const checkAllPost = data => {
    return post(
        {
            url: "/check",
            data
        }
    )
}


// ############### data #########################################

export const getDataGet = data => {
    return get(
        {
            url: "/pic/data",
            data
        }
    )
}

// ###################### system ##########################################

export const getSysProcessGet = data => {
    return get(
        {
            url: "/sys/status/process",
            data
        }
    )
}

export const getProcessInfoPost = data => {
    return post(
        {
            url: "/sys/status/process/info",
            data
        }
    )
}

export const processKillPost = data => {
    return post(
        {
            url: "/sys/status/process/kill",
            data
        }
    )
}


export const getSysNetworkGet = data => {
    return get(
        {
            url: "/sys/status/network",
            data
        }
    )
}

export const getIptablesGet = data => {
    return get(
        {
            url: "/sys/iptables/select",
            data
        }
    )
}

export const addRulePost = data => {
    return post(
        {
            url: "/sys/iptables/cfg",
            data
        }
    )
}

export const deleteRuleDel = data => {
    return del(
        {
            url: "/sys/iptables/del",
            data
        }
    )
}

// ######################### black list ####################################

export const configBlackPost = data => {
    return post(
        {
            url: "/black/cfg",
            data
        }
    )
}

export const showBlackPost = data => {
    return post(
        {
            url: "/black/show",
            data
        }
    )
}

export const deleteLocalDel = data => {
    return del(
        {
            url: "/black/local/del",
            data
        }
    )
}

export const deleteDenyDel = data => {
    return del(
        {
            url: "/black/deny/del",
            data
        }
    )
}



