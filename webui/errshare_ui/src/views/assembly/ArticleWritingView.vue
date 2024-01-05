<template>
    <div id="articlewriting">
        <div>
            <span style="color: #606266"><b>文章标题: </b></span>
            <el-input v-model="titleTxt" style="width: 50%;" placeholder="输入文章标题" />
        </div>

        <div  style="margin-top: 20px;">
          <span style="color: #606266">文章分类: </span>
          <el-select v-model="classValue" placeholder="选择分类">
            <el-option
              v-for="item in assortList"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>

          <span style="margin-left: 80px; color: #606266">文章标签: </span>
          <el-select v-model="labelValue" placeholder="选择标签">
            <el-option
              v-for="item in assortList"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>

        <div style="border: 1px solid #ccc; margin-top: 20px;">
          <Toolbar
            style="border-bottom: 1px solid #ccc"
            :editor="editorRef"
            :defaultConfig="toolbarConfig"
            :mode="mode"
          />
          <Editor
            style="height: 400px; overflow-y: hidden;"
            v-model="valueHtml"
            :defaultConfig="editorConfig"
            :mode="mode"
            @onCreated="handleCreated"
          />
        </div>
        <div style="margin-top: 15px;"><el-button type="primary" @click="getAllcontent()">发布文章</el-button></div>
    </div>

</template>

<script>
  // export default {
  //   name: "articleWritingView"
  // }

import '@wangeditor/editor/dist/css/style.css' // 引入 css

import { onBeforeUnmount, ref, shallowRef, reactive, toRefs,} from 'vue'
import { ElMessage } from 'element-plus'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import {showWzClassGet, contentWritePost} from '@/utils/apis'

export default {
  name: "articleWritingView",
  components: { Editor, Toolbar },
  setup() {
    const data=reactive({
      assortList: [],
      

    })
    const classValue = ref('')
    const labelValue = ref('')
    const titleTxt = ref('')

    function getAllData(){
        showWzClassGet().then(
          res => {
                    data.assortList=res.wz_class
                    // console.log("------->", res)                
            }
        )
    }
    getAllData()

    // 编辑器实例，必须用 shallowRef
    const editorRef = shallowRef()
    // 内容 HTML
    const valueHtml = ref('')

    const toolbarConfig = {
      // excludeKeys: ["insertLink", "insertImage", "editImage", "viewImageLink", "insertVideo", "emotion", "fullScreen"],
    }
    const editorConfig = { placeholder: '飒飒西风满院栽，蕊寒香冷蝶难来。他年我若为青帝，报与桃花一处开。', MENU_CONF: {} }

    // 组件销毁时，也及时销毁编辑器
    onBeforeUnmount(() => {
        const editor = editorRef.value
        if (editor == null) return
        editor.destroy()
    })

    const handleCreated = (editor) => {
      editorRef.value = editor // 记录 editor 实例，重要！
    }

    // 发布后ok后清除页面内容
    function rest(){
      // location.reload();
      classValue.value = ''
      labelValue.value = ''
      titleTxt.value = ''
      valueHtml.value = ''
    }

    function getAllcontent(){
      // console.log("echo ----> ", valueHtml.value, titleTxt.value, classValue.value, labelValue.value)
      contentWritePost(
          {
            "user": localStorage.getItem('user'),
            "title": titleTxt.value,
            "classs": classValue.value,
            "label": labelValue.value,
            "textHtml": valueHtml.value
          }
        ).then(
        res => {
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
                  rest()
              }
      )
    }


    // 上传图片
    editorConfig.MENU_CONF["uploadImage"] = {
              server: 'http://192.168.1.119:8088/wz/upload/images',
              // headers: { Authorization: 'token' },
              fieldName: 'file',
              maxFileSize: 10 * 1024 * 1024, // 最大不能超过10M
              maxNumberOfFiles: 10,    // 最多上传10个文件
              allowedFileTypes: [],
              timeout: 8 * 1000,   //超时 8s
        }


    // 上传视频
    editorConfig.MENU_CONF["uploadVideo"] = {
              server: 'http://192.168.1.119:8088/wz/upload/video',
              // headers: { Authorization: 'token' },
              fieldName: 'video',
              maxFileSize: 1024 * 1024 * 1024, // 最大1G
              timeout: 120 * 1000,   //超时 120s
        }


    
    return {
      ... toRefs(data),
      editorRef,
      valueHtml,
      mode: 'default', // 或 'simple'
      toolbarConfig,
      editorConfig,
      handleCreated,
      classValue,
      labelValue,
      titleTxt,
      getAllcontent,
    };
  }
}
</script>



<style scoped>

</style>