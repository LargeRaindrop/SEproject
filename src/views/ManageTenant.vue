<template>
    <div>
        <Navigator></Navigator>
        <top_bar></top_bar>
        这是一个新页面
        <container_admin_3></container_admin_3>
    </div>
</template>

<script>
    import container_admin_3 from "@/components/container_admin_3";
    import top_bar from "@/components/top_bar";
    import Navigator from "@/components/Navigator";
    export default {
        name: "ManageTenant",
        components:{
            container_admin_3,
            top_bar,
            Navigator
        }
    }
</script>

<style scoped>

</style>