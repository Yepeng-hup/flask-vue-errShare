<template>
  <div>
    <el-alert effect="dark" title="注意！Linux黑名单只对调用了tcp_wrappers和编译libwrap.so的才起作用，可以用ldd命令查看是否支持。" type="error" />
  </div>

  <div class="bj" style="margin-top: 15px">
    <el-form :model="fromData" label-width="120px" style="width: 50%">
      <el-form-item label="服务名" prop="service">
        <el-input v-model="fromData.serviceName" />
      </el-form-item>
      <el-form-item label="IP地址" prop="ip">
        <el-input v-model="fromData.ip" />
      </el-form-item>
      <el-form-item label="黑名单类型">
        <el-checkbox-group v-model="fromData.type">
          <el-checkbox label="deny" name="type" />
          <el-checkbox label="local" name="type" />
        </el-checkbox-group>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="configBlacklist">加入黑名单</el-button>
        <el-button @click="table = true">查看黑名单</el-button>
      </el-form-item>
    </el-form>

    <el-drawer
        v-model="table"
        direction="rtl"
        size="35%"
        title="黑名单详情  (需点击才会有数据和刷新)"
    >
      <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane label="local" name="local">
          <el-table :data="localData" style="width: 100%">
            <el-table-column label="地址" prop="address" width="300"/>
            <el-table-column label="操作" width="100">
              <template #default="scope">
                    <el-button type="danger" @click="localDel(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="deny" name="deny">
          <el-table :data="denyData" style="width: 100%">
            <el-table-column label="服务+地址" prop="ruleStr" width="300"/>
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button type="danger" @click="denyDel(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-drawer>

  </div>

</template>

<script>
import {reactive, toRefs, ref} from "vue";
import {configBlackPost, showBlackPost, deleteLocalDel} from "@/utils/apis";
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";
export default {
  name: "SysBlacklistView",
  setup(){
    const data = reactive({
      fromData: {
        ip: '',
        serviceName: '',
        type: [],
      },
      localData: [],
      denyData: [],
    })

    const rest = ()=>{
      data.fromData.serviceName = ''
      data.fromData.ip = ''
      data.fromData.type = []
    }

    const table = ref(false)
    const activeName = ref('local')
    const router = useRouter();
    const handleClick = function(tab) {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      showBlackPost({"name": tab.paneName}).then(
          res => {
            if (res.s_name === "local"){
              data.localData = res.local_data;
            }else {
              data.denyData = res.deny_data;
            }
          }
      )
    }

    const configBlacklist = () =>{
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      configBlackPost(data.fromData).then(
          res => {
            if (res.code !== 200) {
              ElMessage(
                  {
                    message: res.msg,
                    type: "error",
                    duration: 5000,
                  }
              )
              return
            }
            ElMessage(
                {
                  message: res.msg,
                  type: "success",
                  duration: 5000,
                }
            )
            rest()
          }
      )
    }

    const localDel = row=>{
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      const {address} = row
      deleteLocalDel({"ip": address}).then(
          res => {
            if (res.code !== 200) {
              ElMessage(
                  {
                    message: res.msg,
                    type: "error",
                    duration: 5000,
                  }
              )
              return
            }
            ElMessage(
                {
                  message: res.msg,
                  type: "success",
                  duration: 5000,
                }
            )
          }
      )
    }

    const denyDel = ()=>{

    }

    return {
      ...toRefs(data),
      configBlacklist,
      table,
      activeName,
      handleClick,
      localDel,
      denyDel,
    }

  }
}
</script>

<style scoped>
.bj {
  box-sizing: border-box;
  display: block;
  width: 100%;
  padding: 10px;
  background: #fff;
}
.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>