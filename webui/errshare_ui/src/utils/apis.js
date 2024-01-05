import {post, get, del} from "./axiosPlus"
// import { useRouter} from "vue-router";


// const router = useRouter();
// const checkTokenToLogin = () => {
//     console.log(router)
//     if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == "nill"){
//         router.push({ name: 'loginView' });
//     }  
// }


// 测试接口
export const userLoginPost = data=>{
    return post(
        {
            url: "/tt",
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
    // checkTokenToLogin()
    return get(
        {
            url: "/test/class",
            data
        }
    )
}



//每个请求封装成单个函数
// ############################## 用户相关 #####################################
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

export const updateUserPwdPost = data=>{
    return post(
        {
            url: "/user/update/passwd",
            data
        }
    )
}


// ############################## 文章相关 #####################################

export const contentWritePost = data=>{
    return post(
        {
            url: "/wz/w",
            data
        }
    )
}