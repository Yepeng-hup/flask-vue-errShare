<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item>文章管理</el-breadcrumb-item>
      <el-breadcrumb-item>文章编写</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
  <div id="articlewriting" style="margin-top: 15px">
    <div>
      <span style="color: #606266"><b>文章标题: </b></span>
      <el-input v-model="titleTxt" style="width: 50%;" placeholder="输入文章标题"/>
    </div>

    <div style="margin-top: 20px;">
      <span style="color: #606266">文章分类: </span>
      <el-select v-model="classValue" placeholder="选择分类">
        <el-option
            v-for="item in classList"
            :key="item.value"
            :label="item.label"
            :value="item.value"
        />
      </el-select>

      <span style="margin-left: 80px; color: #606266">文章标签: </span>
      <el-select v-model="labelValue" placeholder="选择标签">
        <el-option
            v-for="item in labelList"
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
    <div style="margin-top: 15px;">
      <el-button type="primary" @click="getAllcontent()">发布文章</el-button>
    </div>
  </div>

</template>

<script>

import '@wangeditor/editor/dist/css/style.css'
import {onBeforeUnmount, ref, shallowRef, reactive, toRefs} from 'vue'
import {ElMessage} from 'element-plus'
import {Editor, Toolbar} from '@wangeditor/editor-for-vue'
import {useRouter} from "vue-router";
import {showWzClassGet, contentWritePost, showWzLabelGet} from '@/utils/apis'
import { ArrowRight } from '@element-plus/icons-vue';

export default {
  name: "articleWritingView",
  components: {Editor, Toolbar},
  setup() {
    const data = reactive({
      classList: [],
      labelList: [],

    })

    const classValue = ref('')
    const labelValue = ref('')
    const titleTxt = ref('')
    const router = useRouter();

    function getAllData() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      showWzClassGet().then(
          res => {
            data.classList = res.wz_class
          }
      )

      //
      showWzLabelGet().then(
          res => {
            data.labelList = res.wz_label
          }
      )
    }

    getAllData()

    const editorRef = shallowRef()
    const valueHtml = ref('')

    const toolbarConfig = {
      // excludeKeys: ["insertLink", "insertImage", "editImage", "viewImageLink", "insertVideo", "emotion", "fullScreen"],
    }
    const editorConfig = {placeholder: '飒飒西风满院栽，蕊寒香冷蝶难来。他年我若为青帝，报与桃花一处开。', MENU_CONF: {}}

    onBeforeUnmount(() => {
      const editor = editorRef.value
      if (editor == null) return
      editor.destroy()
    })

    const handleCreated = (editor) => {
      editorRef.value = editor
    }

    function rest() {
      // location.reload();
      classValue.value = ''
      labelValue.value = ''
      titleTxt.value = ''
      valueHtml.value = ''
    }

    function getAllcontent() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
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
            if (res.code != 200) {
              ElMessage(
                  {
                    message: "发布失败",
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


    const iUrl = process.env.VUE_APP_SERVER_HOST
    editorConfig.MENU_CONF["uploadImage"] = {
      server: `${iUrl}/wz/upload/images`,
      headers: {Authorization: 'Bearer ' + localStorage.getItem('userToken')},
      fieldName: 'file',
      maxFileSize: 10 * 1024 * 1024,
      maxNumberOfFiles: 10,
      allowedFileTypes: [],
      timeout: 8 * 1000,
    }


    editorConfig.MENU_CONF["uploadVideo"] = {
      server: `${iUrl}/wz/upload/video`,
      headers: {Authorization: 'Bearer ' + localStorage.getItem('userToken')},
      fieldName: 'video',
      maxFileSize: 1024 * 1024 * 1024,
      timeout: 120 * 1000,
    }

    return {
      ...toRefs(data),
      editorRef,
      valueHtml,
      mode: 'default',
      toolbarConfig,
      editorConfig,
      handleCreated,
      classValue,
      labelValue,
      titleTxt,
      getAllcontent,
      ArrowRight,
    };
  }
}
</script>
