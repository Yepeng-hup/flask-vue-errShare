<template>
  <el-row :gutter="40">

    <el-col :span="12"><div class="grid-content ep-bg-purple" />
      <div style="background: #fff; border: 1px solid rgb(249, 244, 244);">
        <h4 style="padding: 5px; color: #606266;">服务检测</h4>
        <el-divider border-style="dashed" />
        <div style="padding: 10px;">
          <el-button type="success" @click="checkAll('mongoCheck')">mangodb检测</el-button>
          <el-button type="success" @click="checkAll('siteCheck')">站点检测</el-button>
          <el-button type="success" @click="checkDisk('serverCheck')">服务器检测</el-button>
        </div>
        <div id="check-text" :style="{ padding: '10px', color: check === 'stop' ? 'red' : 'green' }">
          {{ msg }}
        </div>
        <el-divider border-style="dashed" />
        <ul class="infinite-list" style="overflow: auto; margin-top: 10px;">
          <el-table :data="diskList" style="width: 100%">
              <el-table-column prop="DiskName" label="磁盘名"/>
              <el-table-column prop="Total" label="总空间"/>
              <el-table-column prop="Used" label="已用空间"/>
              <el-table-column prop="Free" label="剩余空间"/>
              <el-table-column prop="UsageRate" label="使用率"/>
          </el-table>
        </ul>
      </div>
    </el-col>

    <el-col :span="12"><div class="grid-content ep-bg-purple" />
      <div style="background: #fff; border: 1px solid rgb(249, 244, 244);">
        <h2 style="margin-top: 10px; color: #606266; margin-left: 10px;">TOP 20</h2>
        <p style="margin-left: 10px; color: #606266; font-size: 12px; ">用户最近登录记录</p>
        <ul class="infinite-list" style="margin-top: 10px;">
            <el-table :data="loginInfoList" style="width: 100%">
                <el-table-column prop="user" label="登录用户"/>
                <el-table-column prop="date" label="登录时间"/>
            </el-table>
          </ul>
      </div>
    </el-col>

  </el-row>
</template>
  
<script>
import { reactive, toRefs } from 'vue'
import {getLoginInfoGet, checkAllPost} from "@/utils/apis"
import { ElMessage } from 'element-plus'

  export default {
    name: "homeView",
    setup(){
      const data=reactive({
        loginInfoList:[],
        check: '',
        msg: '',
        diskList: [],

    })

      function showLoginInfo(){
          getLoginInfoGet().then(
            res => {
              data.loginInfoList = res.login_info_list
            }
          )
      }

      showLoginInfo()

      function checkAll(s){
        checkAllPost(
          {
            "action": s,
          }
        ).then(
        res => {
                  if (res.code != 200){
                      ElMessage(
                        {
                            message: "检测失败",
                            type: "error",
                            duration: 5000,
                        }
                      )
                      data.check = "stop"
                      data.msg = res.msg
                    return
                  }
                  ElMessage(
                    {
                        message: "检测成功",
                        type: "success",
                        duration: 5000,
                    }
                  )
                  data.check = "running"
                  data.msg = res.msg
              }
          )
      }

      function checkDisk(s){
        checkAllPost(
          {
            "action": s,
          }
        ).then(
        res => {
                data.diskList = res.msg
              }
          )
      }

      return {
        ...toRefs(data),
        checkAll,
        checkDisk,
      }
    }
  }
</script>

<style scoped>

</style>