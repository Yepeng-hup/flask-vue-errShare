import {post, get, del} from "./axiosPlus"


// 测试接口
export const userLoginPost = data=>{
    return post(
        {
            url: "/err/login",
            data
        }
    )
}

export const showArticleGet = data=>{
    return get(
        {
            url: "/test/art",
            data
        }
    )
}


export const showClassGet = data=>{
    return get(
        {
            url: "/test/class",
            data
        }
    )
}



//每个请求封装成单个函数
export const showUserGet = data=>{
    return get(
        {
            url: "/user/get",
            data
        }
    )
}

export const searchUserGet = data=>{
    return get(
        {
            url: "/user/search",
            data
        }
    )
}

export const createUserPost = data=>{
    return post(
        {
            url: "/user/create",
            data
        }
    )
}

export const updateUserPost = data=>{
    return post(
        {
            url: "/user/update",
            data
        }
    )
}


export const delUserDelete = data=>{
    return del(
        {
            url: "/user/delete",
            data
        }
    )
}

export const showWzClassGet = data=>{
    return get(
        {
            url: "/wz/test",
            data
        }
    )
}