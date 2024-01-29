<template>

  <div class="bj" style="margin-top: 15px">
    <ul class="infinite-list" style="overflow: auto; margin-top: 10px;">
      <el-table :data="networkList" style="width: 100%">
        <el-table-column prop="laddr" label="源地址和端口" width="200"/>
        <el-table-column prop="pid" label="pid" width="100"/>
        <el-table-column prop="process" label="进程名"/>
        <el-table-column prop="raddr" label="目标地址和端口"/>
        <el-table-column prop="status" label="状态" width="100"/>
        <el-table-column prop="type" label="类型" width="100"/>
      </el-table>
    </ul>
  </div>

</template>

<script>
import {reactive, toRefs} from "vue";
import {getSysNetworkGet} from "@/utils/apis"
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";
export default {
  name: "SysNetworkView",
  setup(){
    const data = reactive({
      networkList: [],
    })

    const router = useRouter();
    function showNetworkStatus() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getSysNetworkGet().then(
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
            data.networkList = res.network_list;
          }
      )

    }
    showNetworkStatus()


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