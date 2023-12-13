<template>
  <div id="loading" style="align-items: center; text-align: center; justify-content: center; display: flex;">
    <div class="col-md-12" style="align-items: center; text-align: center; justify-content: center; display: flex;">
    
    <div class="row" style="; align-items: center; height: 280px; width: 280px; justify-content: center; display: flex">
      <img
      class="img"
      src="../assets/polaroid.gif"
      alt="loading..."
      width="200"
      />
    </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "LoadingComponent"
};
</script>

<style>
#loading {
  position: absolute;
  z-index: 1000;
  background-color: white;
  height: 100vh;
  width: 100vw;
  text-align: center;
  line-height: 100vh;
}
.img {
  position: relative;
  margin: auto;
  margin-top: 20%;
}
</style>