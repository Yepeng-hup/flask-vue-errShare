<template>
  <div>
    <el-alert title="注意！这里删除就代表彻底删除了。" type="error" effect="dark"/>
  </div>
  <div class="home-centext">
    <span style="color: #606266"><b>回收文章</b>({{ nums }})</span>
    <el-divider border-style="dashed"/>

    <div style="margin-top: 10px;">
      <el-table :data="wzInfoList" style="width: 100%">
        <el-table-column prop="titel" label="标题" width="300"/>
        <el-table-column prop="user" label="作者" width="100"/>
        <el-table-column prop="class" label="分类" width="100"/>
        <el-table-column prop="label" label="标签"/>
        <el-table-column prop="date" label="发布时间"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" @click="revoke(scope.row)">撤销</el-button>
            <el-button type="danger" @click="recoveryDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
          style="margin-top: 20px;"
          small
          background
          layout="prev, pager, next, jumper, sizes, total"
          :total=nums
          :page-sizes="[20,50,100]"
          v-model:current-page="searchParams.pagenum"
          v-model:page-size="searchParams.pagesize"
          @size-change="recFY"
          @current-change="recFY"
      />

    </div>

  </div>
</template>

<script>
import {reactive, toRefs} from "vue"
import {getRecoveryInfoGet, delRecDelete, revokeRecPost} from "@/utils/apis"
import {ElMessage} from 'element-plus'
import {useRouter} from "vue-router";

export default {
  name: "recoveryView",
  setup() {
    const data = reactive({
      wzInfoList: [],
      nums: 0,
      searchParams: {
        query: "",
        pagesize: 20,
        pagenum: 1,
      },
    })

    const router = useRouter();

    function showRecInfo() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getRecoveryInfoGet(data.searchParams).then(
          res => {
            data.wzInfoList = res.recover_list
            data.nums = res.num
          }
      )

    }

    showRecInfo()

    const recoveryDelete = row => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      const {titel} = row
      delRecDelete({"titel": titel, "user": localStorage.getItem("user")}).then(
          res => {
            showRecInfo()
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


    const revoke = row => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      revokeRecPost({"titel": row.titel}).then(
          res => {
            showRecInfo()
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


    const recFY = () => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getRecoveryInfoGet(data.searchParams).then(
          res => {
            data.wzInfoList = res.recover_list
            data.nums = res.num
          }
      )
    }

    return {
      ...toRefs(data),
      recoveryDelete,
      revoke,
      recFY,
    }
  }
}
</script>

<style scoped>
.el-alert {
  margin: 20px 0 0;
}

.el-alert:first-child {
  margin: 0;
}
</style>