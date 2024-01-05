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
        <el-button style="width: 200px; margin-bottom: 25px;" type="primary" @click="login">登录</el-button>
      </div>
      <!-- <div>
        <a href="#" style="float:right;color: #0b87e7;text-decoration: none;">忘记密码?</a>
      </div> -->
    </div>
  </div>
</template>



<script>
import { toRefs, reactive,} from "vue"
import { ElMessage } from 'element-plus'
import { useRouter } from "vue-router";
import axios from "axios";

export default {
    name: "loginView",

    setup() {
        const data=reactive({
            user: "",
            pwd: "",
        })

        const router = useRouter()

        // function resetData(){
        //     data.user = ''
        //     data.pwd = ''
        // }

        const login = ()=>{
          axios.post('http://192.168.1.119:8088/err/login', {
            "username": data.user, 
            "password": data.pwd,
            })  
            .then(res => {  
              if (res.data.code == 200){
                // console.log("lay ----> ", router)
                      router.push(
                          {
                              name: 'layout', 
                              query: {
                                      u: res.data.username,
                                      r: res.data.role,
                                      t: res.data.token,
                              },
                          }
                      )
              }else {
                      router.push('/')
                      // resetData()
                      ElMessage(
                        {
                            message: res.data.msg,
                            type: "error",
                            duration: 3000,
                        }
                      )
                }       

            })  
            .catch(error => {  
              console.error(error); 
            })
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
    background: 	#F0FFFF;
    margin: 0 auto;
    overflow: hidden;
    margin-top: 10%;
}
.page-title{
    text-align: center;
    color: #0b87e7;
}
.sign-box{
    width: 300px;
    margin: 0 auto;
    padding-top: 5px;
}
</style>
