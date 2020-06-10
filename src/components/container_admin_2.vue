<template>
    <div>
        <el-container style="height: 500px; border: 1px solid #eee">
            <el-container>
                <el-header style="text-align: left; font-size: 20px">
                    <el-dropdown>
                        <i class="el-icon-setting" style="margin-right: 15px"></i>
                    </el-dropdown>
                    <span>信息管理</span>
                </el-header>

                <el-main>
                    <el-button type="primary" icon="el-icon-edit" size="medium" round>管理租客</el-button>
                    <el-button type="primary" icon="el-icon-share" size="medium" round>管理师傅</el-button>
                    <el-button type="primary" icon="el-icon-delete" size="medium" round>管理房源</el-button>
                    <el-button type="primary" icon="el-icon-delete" size="medium" round>管理订单</el-button>
                    <!--<el-button type="primary" icon="el-icon-search" size="medium" round>搜索</el-button>
                    <el-button type="primary">上传<i class="el-icon-upload el-icon&#45;&#45;right"></i></el-button>-->
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
    export default {
        name: "container_admin_2"
    }
</script>

<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }

    .el-aside {
        color: #333;
    }
</style>