<template>
  <div id="articlelabel" class="home-centext">
    <div>
      <span style="color: #606266">标签名称: </span>
      <el-input id="label" v-model="labelName" style="width: 40%;" placeholder="输入新标签"/>
      <el-button type="primary" @click="addLabel()" style="margin-left: 10px;">添加标签</el-button>
    </div>
    <el-divider border-style="dashed"/>

    <div>
      <el-table :data="labelInfoList" style="width: 100%">
        <el-table-column prop="label" label="名称"/>
        <el-table-column prop="date" label="创建时间"/>
        <el-table-column prop="num" label="关联文章数"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="danger" @click="deleteLabel(scope.row)" :icon="Delete" circle/>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          style="margin-top: 20px;"
          small
          background
          layout="prev, pager, next, jumper, sizes, total"
          :total="total"
          v-model:current-page="searchParams.pagenum"
          :page-sizes="[5,10,15,20]"
          v-model:page-size="searchParams.pagesize"
          @size-change="labelFY"
          @current-change="labelFY"
      />
    </div>

  </div>
</template>

<script>
import {reactive, toRefs} from "vue"
import {Delete,} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'
import {useRouter} from "vue-router";
import {addLabelPost, getLabelGet, delLabelDelete} from "@/utils/apis"


export default {
  name: "articleLabelView",
  setup() {
    const data = reactive({
      labelInfoList: [],
      labelName: '',
      searchParams: {
        query: "",
        pagesize: 5,
        pagenum: 1,
      },
      total: 0,
    })

    const router = useRouter();

    function rest() {
      data.labelName = ''
    }

    function showAllLabel() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getLabelGet(data.searchParams).then(
          res => {
            data.labelInfoList = res.labelList
            data.total = res.total
          }
      )
    }

    showAllLabel()


    function addLabel() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      addLabelPost(
          {
            "label": data.labelName,
          }
      ).then(
          res => {
            if (res.code != 200) {
              ElMessage(
                  {
                    message: "创建失败",
                    type: "error",
                    duration: 5000,
                  }
              )
              return
            }
            showAllLabel()
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

    const deleteLabel = row => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      delLabelDelete({"label": row.label}).then(
          res => {
            showAllLabel()
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

    const labelFY = () => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getLabelGet(data.searchParams).then(
          res => {
            data.labelInfoList = res.labelList
            data.total = res.total
          }
      )
    }

    return {
      ...toRefs(data),
      Delete,
      addLabel,
      deleteLabel,
      labelFY,
    }
  }
}
</script>