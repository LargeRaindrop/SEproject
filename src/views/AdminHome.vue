<template>
    <div>
        <Navigator></Navigator>
        <el-row>
            <el-col :span="24"><div class="grid-content bg-purple-light">
                <br>欢迎登录，管理员“{{this.adminName}}”先生/女士！<br><br>每天都要有好心情哦 &nbsp; \(￣︶￣*\))<br><br>
            </div></el-col>
        </el-row>

        <container_admin_1></container_admin_1>
        <br><br><br>
        <container_admin_2></container_admin_2>
    </div>
</template>

<script>
    import Navigator from "@/components/Navigator";
    import container_admin_1 from "@/components/container_admin_1";
    import container_admin_2 from "@/components/container_admin_2";
    export default {
        name: "AdminHome",
        components: {
            Navigator,
            container_admin_1,
            container_admin_2
        },
        data(){
            return{
                adminName:"默认"
            }
        }
    }
</script>

<style scoped>
    .el-row {
        margin-bottom: 20px;
    &:last-child {
         margin-bottom: 0;
     }
    }
    .el-col {
        border-radius: 4px;
    }
    .bg-purple-dark {
        background: #99a9bf;
    }
    .bg-purple {
        background: #d3dce6;
    }
    .bg-purple-light {
        background: #e5e9f2;
    }
    .grid-content {
        border-radius: 4px;
        min-height: 36px;
    }
    .row-bg {
        padding: 10px 0;
        background-color: #f9fafc;
    }

</style>