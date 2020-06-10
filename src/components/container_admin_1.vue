<template>
    <div>
        <el-container style="height: 500px; border: 1px solid #eee">
            <el-container>
                <el-header style="text-align: left; font-size: 20px">
                    <el-dropdown>
                        <i class="el-icon-setting" style="margin-right: 15px"></i>
                    </el-dropdown>
                    <span>处理事项</span>
                </el-header>

                <el-main>
                    <!--<el-table :data="tableData">
                        <el-table-column prop="date" label="日期" width="140">
                        </el-table-column>
                        <el-table-column prop="name" label="姓名" width="120">
                        </el-table-column>
                        <el-table-column prop="address" label="地址">
                        </el-table-column>
                    </el-table>-->
                    <el-button type="primary" icon="el-icon-edit" size="medium" round>审核申请</el-button>
                    <el-button type="primary" icon="el-icon-share" size="medium" round>处理投诉</el-button>
                    <el-button type="primary" icon="el-icon-delete" size="medium" round>处理报修</el-button>
                    <!--<el-button type="primary" icon="el-icon-search" size="medium" round>搜索</el-button>
                    <el-button type="primary">上传<i class="el-icon-upload el-icon&#45;&#45;right"></i></el-button>-->
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>



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

<script>
    export default {
        name: "container_admin_2",
        /*data() {
            const item = {
                date: '2016-05-02',
                name: '王小虎',
                address: '上海市普陀区金沙江路 1518 弄'
            };
            return {
                tableData: Array(20).fill(item)
            }
        }*/
    };
</script>