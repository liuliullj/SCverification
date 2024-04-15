<script lang="ts" setup>
import { reactive, ref, watch, onMounted} from "vue"
import { createTableDataApi, deleteTableDataApi, updateTableDataApi, getTableDataApi,getProjectNameApi,getDemandDataApi, CreatDemandDateApi, updateDemandDateApi, deleteDemandDataApi, getDesignDataApi, getPathDataApi, CreatDesignDateApi, updateDesignDateApi, deleteDesignDataApi} from "@/api/table"
import { type CreateOrUpdateTableRequestData, type GetTableData ,type CreateOrUpdateDemandRequestData, type CreateOrUpdateDesignRequestData} from "@/api/table/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { usePagination } from "@/hooks/usePagination"

defineOptions({
  // 命名当前组件
  name: "ElementPlus"
})

const loading = ref<boolean>(false)
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

const {
  paginationData: demandPaginationData,
  handleCurrentChange: demandhandleCurrentChange,
  handleSizeChange: demandhandleSizeChange
} = usePagination();

const {
  paginationData: designPaginationData,
  handleCurrentChange: designhandleCurrentChange,
  handleSizeChange: designhandleSizeChange
} = usePagination();

//region 增
const DEFAULT_FORM_DATA: CreateOrUpdateDesignRequestData = {
  id: undefined,
  pathname: "",
  expression: ""
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<CreateOrUpdateDesignRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const formRules: FormRules<CreateOrUpdateDesignRequestData> = {
  pathname: [{ required: true, trigger: "blur", message: "请输入路径名" }],
  expression: [{ required: true, trigger: "blur", message: "请输入路径表达式" }],
}

const handleCreateOrUpdateDemand = () => {
  formRef.value?.validate((valid: boolean, fields) => {
    if (!valid) return console.error("表单校验不通过", fields)
    loading.value = true
    const api = formData.value.id === undefined ? CreatDesignDateApi : updateDesignDateApi
    api(formData.value,selectedProject.value)
      .then(() => {
        ElMessage.success("操作成功")
        dialogVisible.value = false
        fetchPathData()
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
  ElMessageBox.confirm(`正在删除路径：${row.pathname}，确认删除？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    deleteDesignDataApi(row.id,selectedProject.value).then(() => {
      ElMessage.success("删除成功");
      fetchPathData();
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

//region 改
const handleUpdate = (row: GetTableData) => {
  dialogVisible.value = true
  formData.value = JSON.parse(JSON.stringify(row))
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

// 获取项目对应的需求列表 仅显示执行流程和方法
const demandData = ref([])
const selectedProject = ref([]);
const fetchProjectData = async () =>{
  if (selectedProject.value.length === 0) {
    return;
  }
  const data = await getDesignDataApi({
      projectname: selectedProject.value,
      currentPage: demandPaginationData.currentPage,
      size: demandPaginationData.size
  });
  console.log(data);
  var demandlist = [];
  for (let index = 0; index < data.list.length; index++) {
    const element = data.list[index];
    var tableRow = {
        "id":element['id'],
        "demandname":element['demandname'],
        "category":element['category'],
        "demanddescription":element['demanddescription'],
        "parentD":element['parentD'],
        "creatTime":element['creatTime']
    };
    demandlist.push(tableRow);
  }
  demandPaginationData.total = data.total;
  demandData.value = demandlist;

  // getDesignDataApi({
  //   projectname: selectedProject.value,
  //   currentPage: demandPaginationData.currentPage,
  //   size: demandPaginationData.size
  // })
  // .then((data) => {
  //   console.log(data)
  //   // console.log("here")
  //   var demandlist = []
  //   for (let index = 0; index < data.list.length; index++){
  //     const element = data.list[index];
  //     var tableRow = {
  //       "id":element[0],
  //       "demandname":element[1],
  //       "category":element[2],
  //       "demanddescription":element[3],
  //       "parentD":element[4],
  //       "creatTime":element[5]
  //     }
  //     demandlist.push(tableRow)
  //   }
  //   demandPaginationData.total = data.total
  //   demandData.value = demandlist
  //   })
}

/** 监听分页参数的变化 */




//获取项目对应的设计路径列表
const designData = ref([])
const fetchPathData = async () =>{
  if (selectedProject.value.length === 0) {
    return;
  }
  const data = await getPathDataApi({
      projectname: selectedProject.value,
      currentPage: designPaginationData.currentPage,
      size: designPaginationData.size
  });
  console.log(data)
  var designlist = [];
  for(let index = 0; index < data.list.length; index++){
    const element = data.list[index];
    var tableRow = {
      'id': element['id'],
      'pathname':element['pathname'],
      'expression':element['expression'],
      'creatTime':element['creatTime']
    }
    designlist.push(tableRow)
  }
  designPaginationData.total = data.total
  designData.value = designlist
  // getPathDataApi({
  //   projectname: selectedProject.value,
  //   currentPage: designPaginationData.currentPage,
  //   size: designPaginationData.size
  // })
  // .then((data)=>{
  //   console.log("getpath")
  //   console.log(data)
  //   var designlist = [];
  //   for(let index = 0; index < data.list.length; index++){
  //     const element = data.list[index];
  //     var tableRow = {
  //       'id': element[0],
  //       'pathname':element[1],
  //       'expression':element[2],
  //       'creatTime':element[3]
  //     }
  //     designlist.push(tableRow)
  //   }
  //   designPaginationData.total = data.total
  //   designData.value = designlist
  // })
}

/** 监听分页参数的变化 */
watch([() => demandPaginationData.currentPage, () => demandPaginationData.pageSize], fetchProjectData, { immediate: false })
watch([() => designPaginationData.currentPage, () => designPaginationData.pageSize], fetchPathData, { immediate: false })

const handleChange = async () => {
  try {
    // 等待第一个fetch操作完成
    await fetchProjectData();
    // 第一个操作完成后，执行第二个fetch操作
    await fetchPathData();
  } catch (error) {
    console.error('操作失败', error);
  }
};

</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <label for="project-select">请选择一个项目：</label>
      <el-select v-model="selectedProject" placeholder="请选择一个项目" size=“large” style="width: 240px" @change="handleChange" @click="fetchProjectNames">
        <el-option
          v-for="name in projectNames"
          :key="name"
          :label="name"
          :value="name">
        </el-option>
      </el-select>
    </el-card>
    <el-card v-loading="loading" shadow="never">
      <div class="header-with-icon">
        <el-icon class="header-icon"><document /></el-icon>
        <span>需求中的执行流程及方法（可达路径节点）</span>
      </div>
      <div class="table-wrapper">
        <el-table :data="demandData">
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column prop="id" label="需求Id" align="center" />
          <el-table-column prop="demandname" label="需求名称" align="center" />
          <el-table-column prop="category" label="需求类别" align="center" />
          <el-table-column prop="demanddescription" label="需求描述" align="center" />
          <el-table-column prop="parentD" label="父需求" align="center" />
        </el-table>
      </div>
      <div class="pager-wrapper">
        <el-pagination
          background
          :layout="demandPaginationData.layout"
          :page-sizes="demandPaginationData.pageSizes"
          :total="demandPaginationData.total"
          :page-size="demandPaginationData.pageSize"
          :currentPage="demandPaginationData.currentPage"
          @size-change="demandhandleSizeChange"
          @current-change="demandhandleCurrentChange"
        />
      </div>





      <div class="header-with-icon">
        <el-icon class="header-icon"><edit /></el-icon>
        <span>可达路径列表</span>
      </div>
      <div class="toolbar-wrapper">
        <div>
          <el-button type="primary" :icon="CirclePlus" @click="dialogVisible = true">新增路径</el-button>
          <el-button type="danger" :icon="Delete">批量删除</el-button>
        </div>
        <div>
          <el-tooltip content="刷新当前页">
            <el-button type="primary" :icon="RefreshRight" circle @click="fetchPathData" />
          </el-tooltip>
        </div>
      </div>
      <div class="table-wrapper">
        <el-table :data="designData">
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column prop="id" label="路径Id" align="center" />
          <el-table-column prop="pathname" label="路径名称" align="center" />
          <el-table-column prop="expression" label="路径表达式" align="center" />
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
          :layout="designPaginationData.layout"
          :page-sizes="designPaginationData.pageSizes"
          :total="designPaginationData.total"
          :page-size="designPaginationData.pageSize"
          :currentPage="designPaginationData.currentPage"
          @size-change="designhandleSizeChange"
          @current-change="designhandleCurrentChange"
        />
      </div>
      <el-dialog
      v-model="dialogVisible"
      :title="formData.id === undefined ? '新增路径' : '修改路径'"
      @closed="resetForm"
      width="30%"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px" label-position="left">
        <el-form-item prop="pathname" label="路径名">
          <el-input v-model="formData.pathname" placeholder="请输入" />
        </el-form-item>
        <el-form-item prop="expression" label="路径表达式">
          <el-input v-model="formData.expression" placeholder="请输入" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateOrUpdateDemand" :loading="loading">确认</el-button>
      </template>
      </el-dialog>
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
</style>
