<script lang="ts" setup>
import { reactive, ref, watch, onMounted} from "vue"
import { getProjectNameApi,getMappingDataApi, CreatMappingDataApi, updateMappingDataApi, deleteMappingDataApi, getBasicDataInputApi} from "@/api/mapping/index"
import { type GetMappingRequestData ,type CreateOrUpdateMappingRequestData} from "@/api/mapping/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { usePagination } from "@/hooks/usePagination"

defineOptions({
  // 命名当前组件
  name: "Mapping"
})

const loading = ref<boolean>(false)
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

//region 增
const DEFAULT_FORM_DATA: CreateOrUpdateMappingRequestData = {
  id: undefined,
  mappingName: "",
  mappingInputBasicData: "",
  mappingOutputBasicData: "",
  demandId: ""
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<CreateOrUpdateMappingRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const formRules: FormRules<CreateOrUpdateMappingRequestData> = {
  mappingName: [{ required: true, trigger: "blur", message: "请输入映射类型名称" }],
  mappingInputBasicData: [{ required: true, trigger: "blur", message: "请输入映射类型输入参数" }],
  mappingOutputBasicData: [{ required: true, trigger: "blur", message: "请输入映射类型输出参数" }],
  demandId: [{ required: true, trigger: "blur", message: "请输入对应需求id" }]
}

const handleCreateOrUpdateMapping = () => {
  formRef.value?.validate((valid: boolean, fields) => {
    if (!valid) return console.error("表单校验不通过", fields)
    if (selectedProject.value.length === 0) {
      ElMessage.success("请先选择一个项目")
      return;
    }
    loading.value = true
    const api = formData.value.id === undefined ? CreatMappingDataApi : updateMappingDataApi
    formData.value.mappingInputBasicData = formData.value.mappingInputBasicData.join(';')
    formData.value.mappingOutputBasicData = formData.value.mappingOutputBasicData.join(';')
    console.log(formData.value)
    api(formData.value,selectedProject.value)
      .then(() => {
        ElMessage.success("操作成功")
        dialogVisible.value = false
        fetchMapping()
      })
      .finally(() => {
        loading.value = false
      })
  })
}
const resetForm = () => {
  formRef.value?.clearValidate()
  formData.value = JSON.parse(JSON.stringify(DEFAULT_FORM_DATA))
}
//endregion

//region 删
const handleDelete = (row) => {
  ElMessageBox.confirm(`正在删除映射类型：${row.mappingName}，确认删除？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    deleteMappingDataApi(row.id,selectedProject.value).then(() => {
      ElMessage.success("删除成功");
      fetchMapping();
    }).catch((error) => {
      // 这里处理API调用失败的情况
      ElMessage.error("删除失败：" + error.message);
    });
  }).catch(() => {
    // 这里处理取消操作的情况
    console.log("取消删除");
  });
};
//#endregion

const mappingInputBasicDataOptions = ref([])
const mappingOutputBasicDataOptions = ref([])
//region 改
const handleUpdate = (row: GetMappingRequestData) => {
  getBasicDataInputApi({projectname: selectedProject.value})
  .then((data) => {
    console.log(data)
    var basicDataInputList = []
    var basicDataOutputList = []
    for (let index = 0; index < data.list.length; index++){
      const element = data.list[index];
      var item = {
        "name":element['name']
      }
      basicDataInputList.push(item)
      basicDataOutputList.push(item)
    }
    mappingInputBasicDataOptions.value = basicDataInputList
    basicDataOutputList.push({'name': 'Null'})
    mappingOutputBasicDataOptions.value = basicDataOutputList
  })
  dialogVisible.value = true
  var mappingData = JSON.parse(JSON.stringify(row))
  mappingData['mappingInputBasicData'] = mappingData['mappingInputBasicData'].split(';')
  mappingData['mappingOutputBasicData'] = mappingData['mappingOutputBasicData'].split(';')
  formData.value = mappingData
}


const handleInsertClick = () => {
  getBasicDataInputApi({projectname: selectedProject.value})
  .then((data) => {
    console.log(data)
    var basicDataInputList = []
    var basicDataOutputList = []
    for (let index = 0; index < data.list.length; index++){
      const element = data.list[index];
      var item = {
        "name":element['name']
      }
      basicDataInputList.push(item)
      basicDataOutputList.push(item)
    }
    mappingInputBasicDataOptions.value = basicDataInputList
    basicDataOutputList.push({'name': 'Null'})
    mappingOutputBasicDataOptions.value = basicDataOutputList
  })
  dialogVisible.value = true
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

// 获取项目对应的映射类型列表
const mappingData = ref([])
const selectedProject = ref([]);
const fetchMapping = () =>{
  if (selectedProject.value.length === 0) {
    return;
  }
  getMappingDataApi({
    projectname: selectedProject.value,
    currentPage: paginationData.currentPage,
    size: paginationData.size
  })
  .then((data) => {
    console.log(data)
    console.log("here")
    var mappinglist = []
    for (let index = 0; index < data.list.length; index++){
      const element = data.list[index];
      var tableRow = {
        "id":element['id'],
        "mappingName":element['mappingName'],
        "mappingInputBasicData":element['mappingInputBasicData'],
        "mappingOutputBasicData":element['mappingOutputBasicData'],
        "demandId":element['demandId'],
        "creatTime":element['creatTime']
      }
      mappinglist.push(tableRow)
    }
    paginationData.total = data.total
    mappingData.value = mappinglist
    })
}

/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], fetchMapping, { immediate: true })

</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <label for="project-select">请选择一个项目：</label>
      <el-select v-model="selectedProject" placeholder="请选择一个项目" size=“large” style="width: 240px" @change="fetchMapping" @click="fetchProjectNames">
        <el-option
          v-for="name in projectNames"
          :key="name"
          :label="name"
          :value="name">
        </el-option>
      </el-select>
    </el-card>
    <el-card v-loading="loading" shadow="never">
      <div class="toolbar-wrapper">
        <div>
          <el-button type="primary" :icon="CirclePlus" @click="handleInsertClick">新增映射类型</el-button>
          <el-button type="danger" :icon="Delete">批量删除</el-button>
        </div>
        <div>
          <el-tooltip content="刷新当前页">
            <el-button type="primary" :icon="RefreshRight" circle @click="fetchMapping" />
          </el-tooltip>
        </div>
      </div>
      <div class="table-wrapper">
        <el-table :data="mappingData">
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column prop="id" label="映射类型Id" align="center" />
          <el-table-column prop="mappingName" label="映射类型名称" align="center" />
          <el-table-column prop="mappingInputBasicData" label="映射类型输入参数" align="center" />
          <el-table-column prop="mappingOutputBasicData" label="映射类型输出参数" align="center" />
          <el-table-column prop="demandId" label="对应需求id" align="center" />
          <el-table-column prop="creatTime" label="创建时间" align="center" />
          <el-table-column fixed="right" label="操作" width="150" align="center">
            <template #default="scope">
              <el-button type="primary" text bg size="small" @click="handleUpdate(scope.row)">修改</el-button>
              <el-button type="danger" text bg size="small" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pager-wrapper">
        <el-pagination
          background
          :layout="paginationData.layout"
          :page-sizes="paginationData.pageSizes"
          :total="paginationData.total"
          :page-size="paginationData.pageSize"
          :currentPage="paginationData.currentPage"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    <!-- 新增/修改 -->
    <el-dialog
      v-model="dialogVisible"
      :title="formData.id === undefined ? '新增映射类型' : '修改映射类型'"
      @closed="resetForm"
      width="30%"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="150px" label-position="left">
        <el-form-item prop="mappingName" label="映射类型名称">
          <el-input v-model="formData.mappingName" placeholder="请输入" />
        </el-form-item>
        
        <el-form-item prop="mappingInputBasicData" label="映射类型输入参数">
          <el-select v-model="formData.mappingInputBasicData" multiple placeholder="请选择"  style="width:100%">
            <el-option 
              v-for="item in mappingInputBasicDataOptions" 
              :key="item.name" 
              :label="item.name" 
              :value="item.name" 
            />
          </el-select>
        </el-form-item>

        <el-form-item prop="mappingOutputBasicData" label="映射类型输出参数">
          <el-select v-model="formData.mappingOutputBasicData" multiple placeholder="请选择"  style="width:100%">
            <el-option 
              v-for="item in mappingOutputBasicDataOptions" 
              :key="item.name" 
              :label="item.name" 
              :value="item.name" 
            />
          </el-select>
        </el-form-item>

        <el-form-item prop="demandId" label="对应需求id">
          <el-input v-model="formData.demandId" placeholder="请输入" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateOrUpdateMapping" :loading="loading">确认</el-button>
      </template>
    </el-dialog>
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

</style>
