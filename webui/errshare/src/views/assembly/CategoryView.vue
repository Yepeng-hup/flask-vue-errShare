<template>
    <div id="category" class="home-centext">
        <div>
              <span style="color: #606266">分类名称: </span>
              <el-input v-model="className" id="classs" style="width: 40%;"  placeholder="输入新分类" />
              <el-button type="primary" style="margin-left: 10px;" @click="addClass()">添加分类</el-button>
        </div>
        <el-divider border-style="dashed" />

        <div>
          <el-table :data="classInfoList" style="width: 100%">
                <el-table-column prop="class" label="名称"/>
                <el-table-column prop="date" label="创建时间"/>
                <el-table-column prop="num" label="关联文章数"/>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="danger" @click="deleteClass(scope.row)" :icon="Delete"/>
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
                @size-change="classFY"
                @current-change="classFY"
            />

        </div>
    </div>

  </template>
  
  <script>
  import {reactive, toRefs} from "vue"
  import {Delete,} from '@element-plus/icons-vue'
  import { ElMessage } from 'element-plus'
  import {getClassGet, addClassPost, delClassDelete} from "@/utils/apis"

    export default {
      name: "categoryView",
      setup(){
        const data=reactive({
          classInfoList: [],
          className: '',
          searchParams: {
                  query: "",
                  pagesize: 5,
                  pagenum: 1,
              },
          total: 0,
        })

        function rest(){
          data.className = ''
        }

        function showAllClass(){
          getClassGet(data.searchParams).then(
            res => {
              data.classInfoList=res.classList
              data.total = res.total
            }
          )
        }
        showAllClass()

        function addClass(){
          addClassPost(
          {
            "class": data.className,
          }
        ).then(
        res => {
                  if (res.code != 200){
                      ElMessage(
                        {
                            message: "创建失败",
                            type: "error",
                            duration: 5000,
                        }
                      )
                    return
                  }
                  showAllClass()
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

      const deleteClass=row=>{
              delClassDelete({"class": row.class}).then(
                    res => {
                        showAllClass()
                        if (res.code != 200){
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


          const classFY=()=>{
            getClassGet(data.searchParams).then(
                  res => {
                        data.classInfoList=res.classList
                        data.total=res.total          
                  }
              )
          }


        return {
          ... toRefs(data),
          Delete,
          addClass,
          deleteClass,
          classFY,
        }
      }
    }
  </script>