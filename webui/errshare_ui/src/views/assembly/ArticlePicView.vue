<template>
    <div id="articlepic" class="home-centext">
        <span style="color: #606266"><b>全部文章</b>(211)</span>
        <el-divider direction="vertical" />
        <span style="color: rgb(255, 0, 34);"><b>回收站</b></span>
        <span>(12)</span>
        <el-divider border-style="dashed" />

        <div class="flex">
              <div class="input-box">
              <el-input
                  v-model="keyS"
                  placeholder="搜索文章"
                  class="input-with-select"
              >
              <template #append>
                  <el-button @click="searchArticle()"><el-icon><Search /></el-icon></el-button>
              </template>
              </el-input>
        </div>
          <el-select v-model="classValue" placeholder="所有分类" style="margin-left: 10px;">
                <el-option
                  v-for="item in assortList"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
          </el-select>
          <el-button type="primary" style="margin-left: 10px;" @click="screenClass()">筛选分类</el-button>
          <el-button color="#d1304b" :dark="false" style="margin-left: 10px;">回收站</el-button>
        </div>

        <div style="margin-top: 20px;">
          <el-table :data="wzInfoList" style="width: 100%">
                <el-table-column prop="title" label="标题" width="300" />
                <el-table-column prop="user" label="作者" width="100"/>
                <el-table-column prop="classs" label="分类" width="100"/>
                <el-table-column prop="label" label="标签"/>
                <el-table-column prop="datetime" label="发布时间"/>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" :icon="Edit" @click="editArticle(scope.row)"/>
                        <el-button type="warning" @click="recoveryArticle(scope.row)">回收</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination
                style="margin-top: 20px;"
                small
                background
                layout="prev, pager, next, jumper, sizes, total"
                :total="20"
                :page-sizes="[5,10,15,20]"
            />
        </div>

    </div>
  </template>
  
  <script>
  import {reactive, toRefs} from "vue"
  import {Edit} from '@element-plus/icons-vue'

  import {showArticleGet} from "@/utils/apis"

  export default {
      name: "articlePicView",
      setup(){
        const data=reactive({
          wzInfoList: [],

        })

        function showAllArticle(){
          showArticleGet().then(
            res => {
              data.wzInfoList=res.wzList
              console.log(res)
            }
          )
        }
        showAllArticle()

        return {
          ... toRefs(data),
          Edit,

        }

      }

  };
  </script>