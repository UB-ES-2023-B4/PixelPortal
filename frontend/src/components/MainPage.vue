<template>
  <div>
    <link
      href="https://unpkg.com/boxicons@2.1.1/css/boxicons.css"
      rel="stylesheet"
    />
    <div class="image-container">
      <div class="search-box">
        <i class="bx bx-search"></i>
        <input type="text" v-model="search" placeholder="Search" />
      </div>

      <div class="images">
        <div
          class="image-card"
          v-for="img in filteredList"
          :key="img.id"
          :data-name="img.username"
        >
          <img :src="require(`@/assets/${img.image}`)" />
          <h6 class="image-title">{{ img.title }}</h6>
          <h6 class="image-username">{{ img.username }}</h6>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  data() {
    return {
      search: "",
      imageList: [
        {
          id: 1,
          image: "placeholder.jpg",
          title: "Landscape",
          description: "cool Landscape",
          username: "Marti",
        },
        {
          id: 2,
          image: "placeholder.jpg",
          title: "Landscape2",
          description: "cool Landscape2",
          username: "Christian",
        },
        {
          id: 3,
          image: "placeholder.jpg",
          title: "Landscape3",
          description: "cool Landscape3",
          username: "Sergio",
        },
      ],
    };
  },
  computed: {
    filteredList() {
      // Check if the first character of the search string is "@"
      if (this.search.length > 0 && this.search.charAt(0) === "@") {
        // Remove the "@" symbol from the search string
        const searchTerm = this.search.substring(1).toLowerCase();

        // Filter and return images based on the modified search term
        return this.imageList.filter((img) => {
          return img.username.toLowerCase().includes(searchTerm);
        });
      } else if (this.search.length > 0 && this.search.charAt(0) === "#") {
        // Remove the "#" symbol from the search string
        const searchTerm = this.search.substring(1).toLowerCase();

        // Filter and return images based on the modified search term
        return this.imageList.filter((img) => {
          return img.title.toLowerCase().includes(searchTerm);
        });
      } else {
        return this.imageList;
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.image-container {
  position: relative;
  min-height: 100vh;
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #fff;
}

.image-container .search-box {
  position: relative;
  height: 42px;
  max-width: 400px;
  margin: 0 auto;
  margin-bottom: 40px;
}

.search-box input {
  position: absolute;
  height: 100%;
  width: 100%;
  outline: none;
  border: none;
  background-color: #323334;
  padding: 0 15px 0 45px;
  color: #fff;
  border-radius: 6px;
  font-size: 20px;
}

.search-box i {
  position: absolute;
  z-index: 2;
  color: #999;
  top: 50%;
  left: 15px;
  font-size: 20px;
  transform: translateY(-50%);
}

.image-container .images .image-card {
  position: relative;
  height: 300px;
  width: 210px;
  border-radius: 6px;
  overflow: hidden;
}

.images {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.images .image-card {
  margin: 8px;
}

.images .image-card img {
  height: 100%;
  width: 100%;
  border-radius: 6px;
  transition: transform 0.2s linear;
}

.image-card:hover img {
  transform: scale(1.15);
}
.image-container .images .image-title {
  position: absolute;
  bottom: 30px;
  left: 10px;
  color: #fff;
  font-size: 24px;
  font-weight: 400;
  text-transform: capitalize;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 3px;
}
.image-container .images .image-username {
  position: absolute;
  bottom: 7.1px;
  left: 10px;
  color: #fff;
  font-size: 20px;
  font-weight: 400;
  text-transform: capitalize;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 3px;
}
</style>
