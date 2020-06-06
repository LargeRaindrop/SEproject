<template>
  <div id="navigator">
    <el-menu
      mode="horizontal"
      :default-active="activeIndex"
      class="el-menu-demo"
      background-color="#9be0f3"
      active-text-color="#fff"
    >
    <div id="nav">
      <el-menu-item index="1" @click="toHome">Home</el-menu-item>
      <!-- <el-menu-item></el-menu-item>-->
    </div>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Navigator',
  props: {
    return: String
  },
  data () {
    return {
      returnType: true,
      activeIndex: '1'
    }
  },
  methods: {
    toHome () {
      this.$router.push({ path: '/' })
    }
  }
}
</script>

<style scoped lang="stylus"></style>

<style scoped>
#nav {
  color: white;
  text-align: left;
  font-size: 20px;
}
</style>
