<template>
  <div class="home">
    <Header></Header>
    <Banner></Banner>
    <Footer></Footer>
  </div>

</template>

<script setup>
  import Header from "../components/Header.vue"
  import Footer from "../components/Footer.vue"
  import Banner from "../components/Banner.vue"

  // import axios from "axios"
  // const http = axios.create()
  // http.get("http://api.luffycity.cn:8000/home/get").then(resp=>{
  //   console.log(resp.data);
  // },(error)=>{
  //   console.log("服务端响应错误");
  //   return Promise.reject(error);
  // })

</script>

<style scoped>

</style>