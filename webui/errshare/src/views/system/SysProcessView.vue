<template>
  <div>
    <el-alert title="系统进程过滤的不是很完善，如需完善自己可以二开，通过json定制指定进程" type="warning" effect="dark"/>
  </div>
  <div class="bj" style="margin-top: 15px">
    <ul class="infinite-list" style="overflow: auto; margin-top: 10px;">
      <el-table :data="processList" style="width: 100%">
        <el-table-column prop="name" label="进程名"/>
        <el-table-column prop="pid" label="pid"/>
        <el-table-column prop="user" label="用户"/>
        <el-table-column prop="memory_percent" label="内存使用率"/>
        <el-table-column label="操作">
          <template #default="scope">

            <el-popover placement="right" :width="800" trigger="click">
              <template #reference>
                <el-button type="primary" @click="catProcessInfo(scope.row)">详细信息</el-button>
              </template>
              <el-table :data="processInfo">
                <el-table-column width="150" prop="ProcessName" label="name"/>
                <el-table-column width="150" prop="ProcessStatus" label="status"/>
                <el-table-column width="150" prop="ProcessStartTime" label="startTime"/>
                <el-table-column width="150" prop="ProcessThreads" label="threads"/>
                <el-table-column width="150" prop="ProcessCPU" label="cpu"/>
                <el-table-column width="150" prop="ProcessReadCount" label="readCount"/>
                <el-table-column width="150" prop="ProcessWriteCount" label="writeCount"/>
                <el-table-column width="150" prop="ProcessReadBytes" label="readBytes"/>
                <el-table-column width="150" prop="ProcessWriteBytes" label="writeBytes"/>
              </el-table>
            </el-popover>
            <el-button type="danger" @click="killProcess(scope.row)">KILL</el-button>
          </template>
        </el-table-column>

      </el-table>
    </ul>
  </div>
</template>

<script>
import {reactive, toRefs, ref} from "vue";
import {getSysProcessGet, getProcessInfoPost, processKillPost} from "@/utils/apis"
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";

export default {
  name: "SysProcessView",
  setup() {
    const data = reactive({
      processList: [],
      processInfo: [],
    })

    const router = useRouter();

    function showSysProcess() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getSysProcessGet().then(
          res => {
            if (res.code != 200) {
              ElMessage(
                  {
                    message: res.msg,
                    type: "error",
                    duration: 5000,
                  }
              )
              return
            }
            data.processList = res.process_list;
          }
      )

    }

    showSysProcess()

    const dialogTableVisible = ref(false)
    const catProcessInfo = row => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      const {pid} = row
      getProcessInfoPost({"pid": pid}).then(
          res => {
            if (res.code != 200) {
              ElMessage(
                  {
                    message: res.msg,
                    type: "error",
                    duration: 5000,
                  }
              )
              return
            }
            data.processInfo = res.process_info
          }
      )

    }


    const killProcess = row => {
      if (localStorage.getItem('userToken') === "undefined" || localStorage.getItem('userToken') === null) {
        router.push({name: 'loginView'});
        return
      }
      const {pid} = row
      processKillPost({"pid": pid}).then(
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
            showSysProcess()
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


    return {
      ...toRefs(data),
      catProcessInfo,
      killProcess,
      dialogTableVisible,
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
</style>