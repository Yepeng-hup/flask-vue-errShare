<template>
    <div id="articlelabel" class="home-centext">
      <div>
              <span style="color: #606266">标签名称: </span>
              <el-input id="classs" style="width: 40%;"  placeholder="输入新标签" />
              <el-button type="primary" style="margin-left: 10px;">添加标签</el-button>
        </div>
        <el-divider border-style="dashed" />

        <div>
          <el-table :data="classInfoList" style="width: 100%">
                <el-table-column prop="labelName" label="名称"/>
                <el-table-column prop="createDate" label="创建时间"/>
                <el-table-column prop="wzMaxNum" label="关联文章数"/>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="danger" @click="deleteLabel(scope.row)" :icon="Delete" circle />
                    </template>
                </el-table-column>
            </el-table>
        </div>

    </div>
  </template>
  
  <script>
  import {Delete,} from '@element-plus/icons-vue'


    export default {
      name: "articleLabelView",
      setup(){
        

        return {
          Delete,
        }
      }
    }
  </script>