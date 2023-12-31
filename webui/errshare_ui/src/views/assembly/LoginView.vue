<template>
    <div class="outer-box">
    <h2 class="page-title">
      ERRSHARE
    </h2>
    <div class="sign-box">
      <div>
        <el-input v-model="user" class="w-50 m-2" placeholder="用户名" />
      </div>
      <div style="margin-top: 10px;">
        <el-input v-model="pwd" type="password" class="w-50 m-2" placeholder="密码" />
      </div>
      <div style="margin-top: 10px; text-align: center;">
        <el-button type="success" @click="login">登录</el-button>
      </div>
      <div>
        <a href="#" style="float:right;color: #5cb85c;text-decoration: none;">忘记密码?</a>
      </div>
    </div>
  </div>
</template>



<script>
import { toRefs, reactive,} from "vue"
import { ElMessage } from 'element-plus'
import { useRouter } from "vue-router";
import {loginPost} from '@/utils/apis'

export default {
    name: "loginView",

    setup() {
        const data=reactive({
            user: "",
            pwd: "",
        })

        const router = useRouter()

        const login = ()=>{
            loginPost({"username": data.user, "password": data.pwd}).then(
                res => {
                            if (res.code == 200){
                                router.push(
                                    {
                                        name: 'layout', 
                                        query: {
                                                u: res.username,
                                                r: res.role,
                                        },
                                    }
                                )
                            }else {
                                router.push('/')
                                ElMessage(
                                  {
                                    //   message: res.msg,
                                      message: "用户名或密码错误",
                                      type: "error",
                                      duration: 3000,
                                  }
                                )
                            }       
                    }
            )
        }

        return {
            ... toRefs(data),
            login,
        }
        
    },
}
</script>


<style scoped>
.outer-box{
    width: 754px;
    background: #efef;
    margin: 0 auto;
    overflow: hidden;
    margin-top: 10%;
}
.page-title{
    text-align: center;
    color: #5cb85c;
}
.sign-box{
    width: 300px;
    margin: 0 auto;
    padding-top: 5px;
}
</style>
