<template>
    <div class="loginregister">
      <LoginRegister />
    </div>
  </template>
  
  <script>
  // @ is an alias to /src
  import LoginRegister from "@/components/LoginRegister.vue";
  
  export default {
    name: "LoginegisterView",
    components: {
      LoginRegister,
    },
  };
  </script>
  