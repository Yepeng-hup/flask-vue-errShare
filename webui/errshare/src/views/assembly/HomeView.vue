<template>
  <div class="home-title">

    <div style="margin-top: 10px;">
      <h2 style="color: #0b87e7">您好！请开始编写今天第一篇文档吧</h2>
      <div style="margin-top: 15px;color: #606266">
        <span><b>每天寄语: </b></span><span>{{ poem }}</span>
      </div>
      <div style="margin-top: 10px;color: #606266">
        <el-row class="my-8 w-[500px]">
          <el-col
              :span="8"
              :xs="24"
              :sm="8"
          >
            <div class="flex items-center">
              <el-icon class="dashboard-icon">
                <avatar/>
              </el-icon>
              总用户数 ({{ userNum }})
            </div>
          </el-col>
        </el-row>
      </div>

      <div id="userpic" style="width: auto; height: 300px; margin-top: 15px"></div>
    </div>

    <div>
      <img src="../../assets/gz.png" style="width: 100%; height: 100%">
    </div>

  </div>

  <el-row :gutter="40">

    <el-col :span="12">
      <div class="grid-content ep-bg-purple"/>
      <div style="background: #fff; border: 1px solid rgb(249, 244, 244);">
        <h4 style="padding: 5px;color: #606266;">服务检测</h4>
        <el-divider border-style="dashed"/>
        <div style="padding: 10px;">
          <el-button type="success" @click="checkAll('mongoCheck')">mangodb检测</el-button>
          <el-button type="success" @click="checkAll('siteCheck')">站点检测</el-button>
          <el-button type="success" @click="checkDisk('serverCheck')">服务器检测</el-button>
        </div>
        <div id="check-text" :style="{ padding: '10px', color: check === 'stop' ? 'red' : 'green' }">
          {{ msg }}
        </div>
        <el-divider border-style="dashed"/>
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

    <el-col :span="12">
      <div class="grid-content ep-bg-purple"/>
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
import {reactive, toRefs} from 'vue'
import {getLoginInfoGet, checkAllPost, getUserDataGet} from "@/utils/apis"
import {useRouter} from "vue-router";
import {ElMessage} from 'element-plus'

export default {
  name: "homeView",
  setup() {
    const data = reactive({
      loginInfoList: [],
      check: '',
      msg: '',
      diskList: [],
      userNum: '',
      poem: '',

    })

    const router = useRouter();

    function showLoginInfo() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getLoginInfoGet().then(
          res => {
            data.loginInfoList = res.login_info_list
            data.poem = res.poem
            data.userNum = res.user_num
          }
      )
    }

    showLoginInfo()

    function checkAll(s) {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      checkAllPost(
          {
            "action": s,
          }
      ).then(
          res => {
            if (res.code != 200) {
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

    function checkDisk(s) {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
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
  },

  mounted() {
    const router = useRouter();
    let d01 = this.$echarts.init(document.getElementById("userpic"));

    function showDataD01() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getUserDataGet().then(res => {
        let xaxisData = res.username_list;
        let seriesData = res.username_num_list;

        d01.setOption({
          title: {text: "TOP500登录次数图"},
          tooltip: {},
          xAxis: {
            data: xaxisData,
          },
          yAxis: {},
          series: [
            {
              name: "次数量",
              type: "bar",
              data: seriesData,
              itemStyle: {
                color: function (params) {
                  if (params.value > 100) {
                    return 'red';
                  } else if (params.value > 50) {
                    return 'yellow'
                  } else {
                    return 'green';
                  }
                }
              }
            },
          ],
        });
      });
    }

    showDataD01();
  },
}
</script>

<style scoped>
.home-title {
  box-sizing: border-box;
  //display: block;
  width: 100%;
  padding: 10px;
  background: #fff;
  margin-top: 15px;
  display: grid;
  grid-template-columns: 1fr 1fr;
}
</style>
