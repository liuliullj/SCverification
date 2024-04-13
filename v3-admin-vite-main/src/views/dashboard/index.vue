<script lang="ts" setup>
import { useUserStore } from "@/store/modules/user"
import Admin from "./components/Admin.vue"
import Editor from "./components/Editor.vue"

const userStore = useUserStore()
const isAdmin = userStore.roles.includes("admin")
</script>

<template>
  <div class="container">
    <h1 class="welcome">欢迎使用智能合约自动化验证系统</h1>
    <div class="info-section">
      <h2 class="intro-title">
        <el-icon><document /></el-icon>
        系统简介
      </h2>
      <p class="intro-text">智能合约自动化验证系统(Smart Contract Automated Verification System,SCAVS)是一款专为智能合约设计和验证而开发的验证工具，旨在为智能合约的开发和部署提供全面、高效、安全的验证服务。
        SCAVS由多个互相协作的模块组成，智能合约需求管理、智能合约设计正确性验证、智能合约安全性验证以及智能合约元语言自动生成等多个模块，确保智能合约在整个生命周期中的每个阶段都得到严格的质量保障。

        在智能合约需求管理方面，本系统采用结构化的方式分析合约需求，通过形式化的规范和精确的需求描述，确保所有合约相关方对合约的预期和目标达成一致。
        智能合约验证模块则基于形式化方法的类型系统理论，对合约的逻辑结构和行为进行验证，以确保合约设计符合预定的规范，并且能够正确地实现业务逻辑，从而避免潜在的功能错误和不一致性。
        安全性验证专注于检测和防范智能合约中常见的安全漏洞，包括溢出漏洞、权限控制漏洞等，降低合约被恶意利用的风险。
        最后，智能合约元语言自动生成模块将经过验证的合约模型转换为易于理解的元语言表示，进一步增强合约一致性、降低维护成本、提升合约可靠性。</p>
    </div>
    <div class="info-section">
      <h2 class="intro-title">
        <el-icon><Guide /></el-icon>
        系统功能模块
      </h2>
      <ul class="feature-list">
        <li>智能合约需求管理</li>
        <li>可验证智能合约建模</li>
        <li>合约正确性验证</li>
        <li>合约安全性验证</li>
        <li>合约元语言生成</li>
      </ul>
    </div>
  </div>
</template>


<style scoped>
.container {
  max-width: 1600px; /* 或者你希望的任何宽度 */
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}

.info-section {
  margin-top: 20px;
}

.welcome{
  color: 	#161657; /* 设置文本颜色为深蓝色 */
  margin-top: 0; /* 减少顶部外边距，使其更靠上 */
  padding-top: 50px; /* 如果需要，可以添加一点内边距以保持一定的间隔 */
}

.intro-title {
  text-align: left; /* 使标题靠左 */
  display: flex; /* 使用flex布局来对齐文本和图标 */
  align-items: center; /* 垂直居中图标和文本 */
  gap: 10px; /* 在图标和文本之间添加一些间隙 */
  padding-top: 30px;
  padding-left: 50px;
  color: 	#161657;
}

.intro-text {
  text-align: left; /* 文本靠左 */
  text-indent: 2em; /* 在文本开始处空两格 */
  font-size: 1.1rem; /* 调大字体大小 */
  line-height: 1.6; /* 增加行间距 */
  margin-left: calc(60px + 10px); /* 调整文本与“系统简介”对齐，24px为假设的图标宽度，10px为gap值 */
  margin-right:30px;
}

.feature-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 15px; /* Increased gap between items */
  justify-content: center;
  margin-left: calc(60px + 10px);
}

.feature-list li {
  background-color: #f0f0f0; /* Default background color */
  padding: 15px; /* Increased padding inside each item */
  border: 1px solid #d0d0d0;
  border-radius: 5px;
  min-width: 180px; /* Increased minimum width */
  text-align: center; /* Center text within each box */
  font-size: 1.5rem;
}

/* Specific background colors for each item */
.feature-list li:nth-child(1) {background-color: RGB(156,212,230);} /* Gold */
.feature-list li:nth-child(2) {background-color: 	RGB(138,208,230);} /* Dark Orange */
.feature-list li:nth-child(3) {background-color: RGB(121,203,230);} /* Slate Blue */
.feature-list li:nth-child(4) {background-color: 	RGB(104,199,230);} /* Pale Green */
.feature-list li:nth-child(5) {background-color: RGB(87,195,230);} /* Pale Turquoise */
</style>
