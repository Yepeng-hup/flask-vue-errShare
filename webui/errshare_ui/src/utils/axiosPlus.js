import axios from "axios";
import { ElLoading, ElMessage} from 'element-plus'

let loadingObj = null
const baseURL = "http://192.168.1.13:8088";  

//创建axios实例，公共使用
const Service = axios.create({
    timeout: 5000,
    baseURL: baseURL,
    headers: {
        //数据类型
        "Content-type": "application/json;charset=utf-8",

        //授权的api,必须传入token
        // "Authorization": "",
    },
})



//请求拦截
Service.interceptors.request.use(
    config => {
        loadingObj=ElLoading.service({
            lock: true,
            text: 'Loading',
            background: 'rgba(0, 0, 0, 0.7)',
          })
          return config
    }
)



//响应拦截

Service.interceptors.response.use(
    response => {
        loadingObj.close()
        return response.data
    },
    error => {
        loadingObj.close()
        ElMessage(
            {
                message: "服务器错误",
                type: "error",
                duration: 5000,
            }
        )
        return error
    },
)


//post / get 

export const post = config => {
    return Service({
            ...config,
            method: "post",
            data: config.data,
        })   
}

export const get = config => {
    return Service({
            ...config,
            method: "get",
            params: config.data,
        })   
}


export const put = config => {
    return Service({
            ...config,
            method: "put",
            params: config.data,
        })   
}

export const del = config => {
    return Service({
            ...config,
            method: "delete",
            params: config.data,
        })   
}