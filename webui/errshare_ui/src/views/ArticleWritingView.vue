<template>
    <div id="articlewriting">
        <div>
            <span style="color: #606266"><b>文章标题: </b></span>
            <el-input v-model="input" style="width: 50%;" placeholder="输入文章标题" />
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
        <div style="margin-top: 15px;"><el-button type="primary" @click="pushWz">发布文章</el-button></div>
    </div>

</template>

<script>
  // export default {
  //   name: "articleWritingView"
  // }

import '@wangeditor/editor/dist/css/style.css' // 引入 css

import { onBeforeUnmount, ref, shallowRef, reactive, toRefs} from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import {showWzClassGet} from '@/utils/apis'

export default {
  name: "articleWritingView",
  components: { Editor, Toolbar },
  setup() {
    const data=reactive({
      assortList: [],
      

    })
    const classValue = ref('')
    const labelValue = ref('')
    const input = ref('')

    function getAllData(){
        showWzClassGet().then(
          res => {
                    data.assortList=res.wz_class
                    console.log("------->", res)                
            }
        )
    }
    getAllData()

    // 编辑器实例，必须用 shallowRef
    const editorRef = shallowRef()
    // 内容 HTML
    const valueHtml = ref('<p>test</p>')

    // 模拟 ajax 异步获取内容
    // onMounted(() => {
    //     setTimeout(() => {
    //         valueHtml.value = '<p>模拟 Ajax 异步设置内容</p>'
    //     }, 1500)
    // })

    const toolbarConfig = {}
    const editorConfig = { placeholder: '请输入内容...' }

    // 组件销毁时，也及时销毁编辑器
    onBeforeUnmount(() => {
        const editor = editorRef.value
        if (editor == null) return
        editor.destroy()
    })

    const handleCreated = (editor) => {
      editorRef.value = editor // 记录 editor 实例，重要！
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
      input,
    };
  }
}
</script>

<style scoped>

</style>