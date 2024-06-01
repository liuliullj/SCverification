<script lang="ts" setup>
import { reactive, ref, watch, onMounted} from "vue"
import { getProjectNameApi, getCallDataApi, verifyCallDataApi, verifyAllDataApi} from "@/api/call/index"
import { type GetCallRequestData, type VerifyCallRequestData} from "@/api/call/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { usePagination } from "@/hooks/usePagination"

defineOptions({
  // 命名当前组件
  name: "Call"
})

const verificationResult = ref("请点击验证按钮进行验证");
const loading = ref<boolean>(false)
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

const {
  paginationData: callPaginationData,
  handleCurrentChange: callhandleCurrentChange,
  handleSizeChange: callhandleSizeChange
} = usePagination();

//region 增
const DEFAULT_FORM_DATA: VerifyCallRequestData = {
  id: "",
  pathId: "",
  pathName: "",
  pathExpression: ""
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<VerifyCallRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))


const verifyCall = (row: GetCallRequestData) => {
  if (selectedProject.value.length === 0) {
    return;
  }
  verificationResult.value = '正在生成验证结果，请稍等...'
  formData.value = JSON.parse(JSON.stringify(row))
  const api = verifyCallDataApi
  api(formData.value,selectedProject.value)
    .then((data) => {
      console.log('###### verifyCall ', data)
      verificationResult.value = data['result'];
    })
    .finally(() => {
      loading.value = false
    })
}


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
const callData = ref([])
const selectedProject = ref([]);
const fetchCallData = async () => {
  try {
    if (selectedProject.value.length === 0) {
      return;
    }
  const data = await getCallDataApi({
      projectname: selectedProject.value,
      currentPage: callPaginationData.currentPage,
      size: callPaginationData.size
  });
  console.log(data);
  var calllist = [];
  for (let index = 0; index < data.list.length; index++) {
    const element = data.list[index];
    var tableRow = {
        "id":element['id'],
        "pathId":element['pathId'],
        "pathName":element['pathName'],
        "pathExpression":element['pathExpression']
    };
    calllist.push(tableRow);
  }
  callPaginationData.total = data.total;
  callData.value = calllist;
  } catch (error) {
    console.error('操作失败', error);
  }
};

const verifyAll = () => {
  console.log('verifyAll call')
  if (selectedProject.value.length === 0) {
    return;
  }
  verificationResult.value = '正在生成验证结果，请稍等...'
  const api = verifyAllDataApi
  api(JSON.stringify(callData.value), selectedProject.value)
    .then((data) => {
      console.log('###### verifyAll ', data)
      verificationResult.value = data['result'];
    })
    .finally(() => {
      loading.value = false
    })
}


/** 监听分页参数的变化 */
watch([() => callPaginationData.currentPage, () => callPaginationData.pageSize], fetchCallData, { immediate: false })


</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <label for="project-select">请选择一个项目：</label>
      <el-select v-model="selectedProject" placeholder="请选择一个项目" size=“large” style="width: 240px" @change="fetchCallData" @click="fetchProjectNames">
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
        <span>可达路径</span>
      </div>
      <div class="table-wrapper">
        <el-table :data="callData">
          <el-table-column type="selection" width="50" align="center" />
          <!-- <el-table-column prop="id" label="Id" align="center" /> -->
          <el-table-column prop="pathId" label="路径编号" align="center"  width="150"/>
          <el-table-column prop="pathName" label="路径名称" align="center" width="250" />
          <el-table-column prop="pathExpression" label="路径表达式" align="center" />
          <el-table-column fixed="right" label="操作" width="150" align="center">
            <template #default="scope">
              <el-button type="primary" text bg size="small" @click="verifyCall(scope.row)">验证</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pager-wrapper">
        <el-pagination
          background
          :layout="callPaginationData.layout"
          :page-sizes="callPaginationData.pageSizes"
          :total="callPaginationData.total"
          :page-size="callPaginationData.pageSize"
          :currentPage="callPaginationData.currentPage"
          @size-change="callhandleSizeChange"
          @current-change="callhandleCurrentChange"
        />
      </div>
      <div class="header-with-icon">
        <el-icon class="header-icon"><edit /></el-icon>
        <span>验证结果</span>
      </div>
      <div class="toolbar-wrapper">
        <div>
          <el-button type="primary" :icon="CirclePlus" @click="verifyAll()">验证全部路径</el-button>
        </div>
      </div>
      <div class="app-container">
        <!-- <el-card header="验证结果">
          <div class="text-display">
            {{ verificationResult }}
          </div>
        </el-card> -->
        <el-card class="box-card" header="验证结果">
          <div slot="header" class="clearfix custom-header scoller-display">
            <span>{{ verificationResult }}</span>
          </div>
      </el-card>
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
  max-height: 300px; /* 最大高度，超过这个高度会显示滚动条 */
  overflow-y: auto; /* 垂直方向上溢出内容时显示滚动条 */
  padding: 10px;
  border: 1px solid #ccc; /* 边框样式 */
  margin: 10px 0;
  white-space: pre-wrap; /* 保留空白符，允许自动和正常的文本换行 */
}
</style>
