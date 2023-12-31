<template>
    <div id="category" class="home-centext">
        <div>
              <span style="color: #606266">分类名称: </span>
              <el-input id="classs" style="width: 40%;"  placeholder="输入新分类" />
              <el-button type="primary" style="margin-left: 10px;">添加分类</el-button>
        </div>
        <el-divider border-style="dashed" />

        <div>
          <el-table :data="classInfoList" style="width: 100%">
                <el-table-column prop="className" label="名称"/>
                <el-table-column prop="createDate" label="创建时间"/>
                <el-table-column prop="wzMaxNum" label="关联文章数"/>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="danger" @click="deleteClass(scope.row)" :icon="Delete"/>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>

  </template>
  
  <script>
  import {reactive, toRefs} from "vue"
  import {Delete,} from '@element-plus/icons-vue'

  import {showClassGet} from "@/utils/apis"

    export default {
      name: "categoryView",
      setup(){
        const data=reactive({
          classInfoList: [],

        })

        function showAllClass(){
          showClassGet().then(
            res => {
              data.classInfoList=res.classList
              console.log(res)
            }
          )
        }
        showAllClass()

        return {
          ... toRefs(data),
          Delete,
        }
      }
    }
  </script>