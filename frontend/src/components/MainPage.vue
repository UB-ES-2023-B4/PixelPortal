<template>
  <div class="container">
    <link
      href="https://unpkg.com/boxicons@2.1.1/css/boxicons.css"
      rel="stylesheet"
    />
    <div class="side-bar">
      <div class="user-info-wrapper">
        <div class="user-info">
          <div class="username-and-picture">
            <img
              src="../assets/default_PFP.png"
              alt="Profile Picture"
              class="profile-picture"
            />
            <h6 class="username">{{ username }}</h6>
          </div>
          <div class="dropdown">
            <button class="options-button" @click="toggleDropdown">
              <i class="bx bx-dots-vertical-rounded"></i>
            </button>
            <div
              id="dropdown-content"
              class="dropdown-content"
              v-if="showDropdown"
            >
              <a href="/">Log out</a>
            </div>
          </div>
        </div>
        <button class="post-button" @click="showUploadImageForm = true">
          <i class="bx bx-plus"></i> Post
        </button>
      </div>
    </div>

    <!-- Image container --->
    <div class="image-container">
      <div class="search-box">
        <i class="bx bx-search"></i>
        <input type="text" v-model="search" placeholder="Search" />
      </div>
      <!-- Popup to upload images component -->
      <UploadImagePopup
        :open="showUploadImageForm"
        :username="username"
        :token="token"
        @close="closeUploadImageForm"
      ></UploadImagePopup>
      <div class="images">
        <div
          class="image-card"
          v-for="img in filteredList"
          :key="img.id"
          :data-name="img.username"
        >
          <img :src="img.image" />
          <h6 class="image-title">{{ img.title }}</h6>
          <h6 class="image-username">{{ img.username }}</h6>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { storage } from "@/firebase";
import { ref as firebaseRef, getDownloadURL } from "firebase/storage";
import UploadImagePopup from "./UploadImagePopup.vue";
import axios from "axios";
export default {
  name: "MainPage",
  components: { UploadImagePopup },
  setup() {
    const showUploadImageForm = ref(false);
    return { showUploadImageForm };
  },
  data() {
    return {
      search: "",
      imageList: [],
      showDropdown: false,
      username: "notLoggedIn",
      token: "",
      postedImageID: "",
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
  methods: {
    toggleDropdown(event) {
      if (event) {
        event.stopPropagation();
      }
      this.showDropdown = !this.showDropdown;
    },
    closeDropdown(event) {
      if (!event.target.classList.contains("options-button")) {
        this.showDropdown = false;
      }
    },
    closeUploadImageForm(data) {
      this.showUploadImageForm = false;
      this.postedImageID = data.imageID;
      //Check if image has been posted
      if (data.hasPosted) {
        console.log("UPLOADED IMAGE UUID: ", this.postedImageID);
        console.log(data);
        //post image with all the data + the image ID to the backend DATABASE here
        const path = "http://localhost:8000/publicaciones";
        const headers = { Authorization: "Bearer " + this.token };
        const dbData = {
          titulo: data.imageTitle,
          descripcion: data.imageDescription,
          imagen_url: data.imageID,
        };
        console.log("POSTING THIS:");
        console.log(dbData);
        axios
          .post(path, dbData, { headers })
          .then((response) => {
            if (response.status === 200) {
              alert("Image uploaded successfully!");
            }
          })
          .catch((error) => {
            alert("Error: " + error.response.data.message);
          });
        //This code is temporary while there is no database:
        const postedImageRef = firebaseRef(
          storage,
          "postedImages/" + this.postedImageID
        );
        getDownloadURL(postedImageRef).then((url) => {
          let image = {
            id: 0,
            image: url,
            description: data.imageDescription,
            title: data.imageTitle,
            username: data.username,
          };
          console.log("IMAGE: ");
          console.log(image);
          this.imageList.push(image);
          console.log(this.imageList);
        });
      }
    },
  },
  mounted() {
    window.addEventListener("click", this.closeDropdown);
  },
  beforeUnmount() {
    window.removeEventListener("click", this.closeDropdown);
  },
  created() {
    this.username = this.$route.query.username;
    this.token = this.$route.query.token;
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
  max-height: 100%;
  max-width: 100%;
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

.container {
  display: flex;
}

.side-bar {
  background-color: rgba(20, 117, 236, 0.9);
  width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding-top: 20px;
  padding-bottom: 20px;
  position: sticky;
  top: 0;
  z-index: 2;
}

.user-info-wrapper {
  position: sticky;
  top: 0;
  background-color: transparent;
  padding: 10px;
  z-index: 3;
  box-shadow: none;
}

.user-info {
  display: flex;
  align-items: center;
}

.username-and-picture {
  display: flex;
  align-items: center;
}

.profile-picture {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
}

.username {
  color: white;
  margin: 0;
}

.options-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}

/* Style the dropdown button and content */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  position: absolute;
  background-color: white;
  min-width: 100px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.show {
  display: block;
}

.post-button {
  background-color: transparent;
  border: none;
  color: white;
  font-size: 16px;
  padding: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  width: 100%;
  margin-top: 20px;
  border-radius: 6px;
}

.post-button i {
  margin-right: 5px;
}

.post-button:hover {
  color: rgba(20, 117, 236, 0.9);
  background-color: white;
  transition: background-color 0.2s linear;
}
</style>
