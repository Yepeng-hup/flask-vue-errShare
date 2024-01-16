<template>
    <div id="articlepic" class="home-centext">
        <span style="color: #606266"><b>全部文章</b>({{ nums }})</span>
        <el-divider border-style="dashed" />

        <div class="flex">
              <div class="input-box">
              <el-input
                  v-model="searchText"
                  placeholder="输入标题关键字"
                  class="input-with-select"
              >
              <template #append>
                  <el-button @click="searchArticle()"><el-icon><Search /></el-icon></el-button>
              </template>
              </el-input>
        </div>
          <el-select v-model="classValue" placeholder="所有分类" style="margin-left: 10px;">
                <el-option
                  v-for="item in classList"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
          </el-select>
          <el-button type="primary" style="margin-left: 10px;" @click="screenClass()">筛选分类</el-button>
        </div>

        <div style="margin-top: 20px;">
          <el-table :data="wzInfoList" style="width: 100%">
                <el-table-column prop="titel" label="标题" width="250" />
                <el-table-column prop="user" label="作者" width="100"/>
                <el-table-column prop="class" label="分类" width="100"/>
                <el-table-column prop="label" label="标签"/>
                <el-table-column prop="date" label="发布时间"/>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" :icon="Edit" @click="editArticle(scope.row)"/>
                        <el-button type="warning" @click="recoveryArticle(scope.row)">回收</el-button>
                        <el-button type="primary" @click="catArticle(scope.row)">查看</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination
                style="margin-top: 20px;"
                small
                background
                layout="prev, pager, next, jumper, sizes, total"
                :total=nums
                :page-sizes="[10,20,50,100]"
                v-model:current-page="searchParams.pagenum"
                v-model:page-size="searchParams.pagesize"
                @size-change="picFY"
                @current-change="picFY"
            />

            
            <!-- 编辑弹窗对话框 -->
            <el-dialog v-model="dialogFormVisible" title="编辑文章"  fullscreen="true">
                <el-form 
                :model="contentHtml"
                label-width="120px"
                class="demo-ruleForm"
                >

                
                  标题: <el-input id="title" style="width: 50%;" v-model="contentHtml.titel"/>
          
                  <div style="border: 1px solid #ccc; margin-top: 20px;">
                    <Toolbar
                      style="border-bottom: 1px solid #ccc"
                      :editor="editorRef"
                      :defaultConfig="toolbarConfig"
                      :mode="mode"
                    />
                    <Editor
                      style="height: 400px; overflow-y: hidden;"
                      v-model="contentHtml.text"
                      :defaultConfig="editorConfig"
                      :mode="mode"
                      @onCreated="handleCreated"
                    />
                  </div>
              </el-form>

                <template #footer>
                    <div style="text-align: center;">
                        <el-button type="danger" @click="cancellation">取消</el-button>
                        <el-button type="primary" @click="updateContent()">更新</el-button>
                    </div>
                </template>

            </el-dialog>     

        </div>

    </div>
  </template>
  
  <script>
  import {reactive, toRefs, shallowRef, onBeforeUnmount} from "vue"
  import {Edit} from '@element-plus/icons-vue'
  import { ElMessage } from 'element-plus'
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
  import '@wangeditor/editor/dist/css/style.css'
  import { useRouter} from "vue-router";
  import {showArticleGet, showWzClassGet, screenClassPost, searchContentPost, delTextDelete, editContentPost, updateContentPost} from "@/utils/apis"

  export default {
      name: "articlePicView",
      components: { Editor, Toolbar },

      setup(){
        const data=reactive({
          wzInfoList: [],
          classList: [],
          classValue: '',
          searchText: '',
          nums: 0,
          searchParams: {
                  query: "",
                  pagesize: 10,
                  pagenum: 1,
              },
          contentHtml: [],
          dialogFormVisible: false,
          
        })


          const editorRef = shallowRef()
          const toolbarConfig = {}
          const editorConfig = { MENU_CONF: {} }
          const router = useRouter();

          onBeforeUnmount(() => {
              const editor = editorRef.value
              if (editor == null) return
              editor.destroy()
          })

          const handleCreated = (editor) => {
            editorRef.value = editor
          }
          const iUrl = process.env.VUE_APP_SERVER_HOST

        editorConfig.MENU_CONF["uploadImage"] = {
                  server: `${iUrl}/wz/upload/images`,
                  headers: { Authorization: 'Bearer '+ localStorage.getItem('userToken') },
                  fieldName: 'file',
                  maxFileSize: 10 * 1024 * 1024,
                  maxNumberOfFiles: 10,
                  allowedFileTypes: [],
                  timeout: 8 * 1000,
            }

        editorConfig.MENU_CONF["uploadVideo"] = {
                  server: `${iUrl}/wz/upload/video`,
                  headers: { Authorization: 'Bearer '+ localStorage.getItem('userToken') },
                  fieldName: 'video',
                  maxFileSize: 1024 * 1024 * 1024,
                  timeout: 120 * 1000,
            }


        function showAllArticle(){
          if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
          showArticleGet(data.searchParams).then(
            res => {
              data.wzInfoList=res.wzList
              data.nums = res.num
            }
          )
          showWzClassGet().then(
            res => {
              data.classList=res.wz_class
            }
          )
        }
        showAllArticle()

        function rest(){
            data.classValue = ''
            data.searchText = ''
        }

        function screenClass(){
          if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
          screenClassPost({"class": data.classValue}).then(
            res => {
              data.wzInfoList=res.wz_list
              data.nums = res.num
              rest()
            }
          )
        }

        function searchArticle(){
          if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
          searchContentPost({"searchTxt": data.searchText}).then(
            res => {
              data.wzInfoList = res.wz_list
              data.nums = res.num
              rest()
            }
          )

        }

        const recoveryArticle=row=>{
          if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
              const {titel} = row 
              delTextDelete({"titel": titel}).then(
                    res => {
                        showAllArticle()
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

          const catArticle=row=>{
            if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
              const {titel} = row
              const url = process.env.VUE_APP_SERVER_HOST
              window.open(`${url}/documents/select/${titel}`, '_blank');
          }

          const picFY=()=>{
            if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
            showArticleGet(data.searchParams).then(
                  res => {
                    data.wzInfoList=res.wzList
                    data.nums = res.num
                  }
              )
          }

          const cancellation=()=>{
              data.dialogFormVisible=false
          }

          function editArticle(text){
            if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
              editContentPost(text).then(
              res => {
                data.dialogFormVisible=true
                data.contentHtml = res.contentHtml
              }
            )
          }

         function updateContent(){
          if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null){
                    router.push({ name: 'loginView' });
                    return
                }
                      updateContentPost({"text": data.contentHtml.text, "title": data.contentHtml.titel}).then(
                          res => {
                              data.dialogFormVisible = false
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


        return {
          ... toRefs(data),
          Edit,
          screenClass,
          searchArticle,
          recoveryArticle,
          picFY,
          editArticle,
          cancellation,
          catArticle,
          updateContent,
          toolbarConfig,
          editorConfig,
          handleCreated,
          mode: 'default',
          editorRef,
        }

      }

  };
  </script>