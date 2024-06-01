<script lang="ts" setup>
import { reactive, ref, watch, onMounted, computed} from "vue"
import { createTableDataApi, deleteTableDataApi, updateTableDataApi, getTableDataApi,getProjectNameApi,getDemandDataApi, CreatDemandDateApi, updateDemandDateApi, deleteDemandDataApi} from "@/api/table"
import { type CreateOrUpdateTableRequestData, type GetTableData ,type CreateOrUpdateDemandRequestData} from "@/api/table/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { usePagination } from "@/hooks/usePagination"
import {generateApi } from "@/api/generate/index"

defineOptions({
  // 命名当前组件
  name: "ElementPlus"
})

const loading = ref<boolean>(false)
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

//region 增
const DEFAULT_FORM_DATA: CreateOrUpdateDemandRequestData = {
  id: undefined,
  demandname: "",
  category: "",
  demanddescription: "",
  parentD: ""
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<CreateOrUpdateDemandRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const formRules: FormRules<CreateOrUpdateDemandRequestData> = {
  demandname: [{ required: true, trigger: "blur", message: "请输入需求名" }],
  category: [{ required: true, trigger: "blur", message: "请输入需求类别" }],
  demanddescription: [{ required: true, trigger: "blur", message: "请输入需求描述" }],
  parentD: [{ required: true, trigger: "blur", message: "请输入父需求Id" }]
}


//endregion



/** 获取项目名称列表*/
onMounted(() => {
  fetchProjectNames();
});
const projectNames = ref([])
const fetchProjectNames = () =>{
  getProjectNameApi({})
  .then(({ data }) => {
    console.log(data)
    projectNames.value = data
    })
}

// 获取项目对应的需求列表
const demandData = ref([])
const selectedProject = ref([]);
const fetchProjectData = () =>{
  if (selectedProject.value.length === 0) {
    return;
  }
  getDemandDataApi({
    projectname: selectedProject.value,
    currentPage: paginationData.currentPage,
    size: paginationData.size
  })
  .then((data) => {
    console.log(data)
    console.log("here")
    var demandlist = []
    for (let index = 0; index < data.list.length; index++){
      const element = data.list[index];
      var tableRow = {
        "id":element['id'],
        "demandname":element['demandname'],
        "category":element['category'],
        "demanddescription":element['demanddescription'],
        "parentD":element['parentD'],
        "creatTime":element['creatTime']
      }
      demandlist.push(tableRow)
    }
    paginationData.total = data.total
    demandData.value = demandlist
    })
}

const genResult = ref("请点击生成按钮进行生成");
const generateLanguage = () => {
  console.log('generate call')
  if (selectedProject.value.length === 0) {
    return;
  }
  genResult.value = '正在生成验证结果，请稍等...'
  const api = generateApi
  api(selectedProject.value)
    .then((data) => {
      console.log('###### generate ', data)
      genResult.value = data['result'];
    })
    .finally(() => {
      loading.value = false
    })
}

/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], fetchProjectData, { immediate: true })

const categoryString = computed({
  get: () => formData.value.category,
  set: (value) => {
    if (Array.isArray(value)) {
      // 如果 value 是数组，取最后一个元素作为 category 值
      formData.value.category = value[value.length - 1] || "";
    } else {
      formData.value.category = value;
    }
  }
});

</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <label for="project-select">请选择一个项目：</label>
      <el-select v-model="selectedProject" placeholder="请选择一个项目" size=“large” style="width: 240px" @change="fetchProjectData" @click="fetchProjectNames">
        <el-option
          v-for="name in projectNames"
          :key="name"
          :label="name"
          :value="name">
        </el-option>
      </el-select>

    </el-card>

    <div class="toolbar-wrapper">
      <div>
        <el-button type="primary" :icon="CirclePlus" @click="generateLanguage()">生成智能合约元语言</el-button>
      </div>
    </div>
    <el-card class="box-card" header="合约元语言">
      <div slot="header" class="clearfix custom-header scoller-display" style="line-height: 2;">
        <span>{{ genResult }}</span>
      </div>
    </el-card>


  </div>
</template>

<style lang="scss" scoped>
.search-wrapper {
  align-items: center;
  margin-bottom: 20px;
  height: 75px;
  :deep(.el-card__body) {
    padding-bottom: 2px;
  }
}

.toolbar-wrapper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.table-wrapper {
  margin-bottom: 20px;
}

.pager-wrapper {
  display: flex;
  justify-content: flex-end;
}

.custom-header {
  margin-top: -10px; /* 根据需要调整这个值 */
}

/* 调整代码段行间距 */
.custom-code {
  line-height: 1.5; /* 增加行高来扩大间距，根据需要调整这个值 */
  margin-top: -10px;
  margin-bottom: -10px;
}

.header-with-icon {
  display: flex;
  align-items: center; /* 保证文本和图标垂直居中 */
  margin-bottom: 20px; /* 调整下边距 */

}

.header-icon {
  margin-right: 8px; /* 在图标和文本之间添加一些间隔 */
}

.header-with-icon span {
  font-size: 18px; /* 增加文本的字体大小 */
}

.text-display {
  max-height: 300px; /* 最大高度，超过这个高度会显示滚动条 */
  overflow-y: auto; /* 垂直方向上溢出内容时显示滚动条 */
  padding: 10px;
  border: 1px solid #ccc; /* 边框样式 */
  margin: 10px 0;
  background-color: #f9f9f9; /* 背景色 */
  white-space: pre-wrap; /* 保留空白符，允许自动和正常的文本换行 */
}

.scoller-display {
  max-height: 800px; /* 最大高度，超过这个高度会显示滚动条 */
  overflow-y: auto; /* 垂直方向上溢出内容时显示滚动条 */
  padding: 10px;
  border: 1px solid #ccc; /* 边框样式 */
  margin: 10px 0;
  white-space: pre-wrap; /* 保留空白符，允许自动和正常的文本换行 */
}
</style>
