<template>
  <el-row :gutter="10">
    <el-col :span="14"><div class="grid-content ep-bg-purple" />
      <div class="bj">
        <ul class="infinite-list" style="overflow: auto; margin-top: 10px;">
          <el-table :data="networkList" style="width: 90%">
            <el-table-column prop="laddr" label="src"/>
            <el-table-column prop="pid" label="pid"/>
            <el-table-column prop="process" label="进程名"/>
            <el-table-column prop="raddr" label="dest"/>
            <el-table-column prop="status" label="状态"/>
            <el-table-column prop="type" label="类型"/>
          </el-table>
        </ul>
      </div>
    </el-col>

    <el-col :span="10"><div class="grid-content ep-bg-purple" />
      <div class="bj">
        <ul class="infinite-list" style="overflow: auto; margin-top: 10px;">
          <el-table :data="processList" style="width: 90%">
            <el-table-column prop="name" label="进程名"/>
            <el-table-column prop="pid" label="pid"/>
            <el-table-column prop="user" label="用户"/>
            <el-table-column prop="memory_percent" label="内存使用率"/>
          </el-table>
        </ul>
      </div>
    </el-col>

  </el-row>

</template>

<script>
import {reactive, toRefs} from "vue";
import {getSysStatusGet} from "@/utils/apis"
export default {
  name: "SysStatusView",
  setup(){
    const data = reactive({
      networkList: [],
      processList: [],
    })

    function showSysStatus() {
      getSysStatusGet().then(
          res => {
            data.networkList = res.network_list;
            data.processList = res.process_list;
          }
      )

    }
    showSysStatus()


    return {
      ...toRefs(data)
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
</style>