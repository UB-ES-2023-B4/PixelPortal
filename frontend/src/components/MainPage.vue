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
              :src="profilePicture"
              alt="Profile Picture"
              class="profile-picture"
            />
            <h6 class="username">{{ username }}</h6>
          </div>
          <div class="dropdown">
            <button class="options-button" @click="toggleUserDropdown">
              <i class="bx bx-dots-vertical-rounded"></i>
            </button>
            <div
              id="dropdown-content"
              class="dropdown-content"
              v-if="showUserDropdown"
            >
              <a href="/">Edit Profile</a>
              <a href="/">Log out</a>
            </div>
          </div>
        </div>
        <button class="post-button" @click="showUploadImageForm = true">
          <i class="bx bx-plus"></i> Post
        </button>
        <button
          class="post-button"
          :class="{ 'post-button-my-images-selected': showMyImages }"
          @click="showMyImages = !showMyImages"
        >
          <img class="sidebar-icon" src="../assets/images.svg" alt="" />
          My Images
        </button>
      </div>
    </div>

    <!-- Image container --->
    <div class="image-container">
      <div class="search-container">
        <div class="search-box">
          <i class="bx bx-search"></i>
          <input type="text" v-model="search" placeholder="Search" />
        </div>
        <div class="dropdown">
          <button class="sort-button" @click="toggleSortDropdown">
            <img class="sort-icon" src="../assets/filter.svg" alt="" />
          </button>
          <div class="dropdown-content" v-if="showSortDropdown">
            <a @click="sortImagesByUploadDate(true)"
              >Sort by upload Date (ascending)</a
            >
            <a @click="sortImagesByUploadDate(false)"
              >Sort by upload Date (descending)</a
            >
            <a>Sort by likes</a>
          </div>
        </div>
      </div>
      <!-- Popup to upload images component -->
      <UploadImagePopup
        :open="showUploadImageForm"
        :username="username"
        :token="token"
        @close="closeUploadImageForm"
      >
      </UploadImagePopup>
      <div class="images">
        <div
          class="image-card"
          v-for="img in showMyImages ? myImagesList : filteredList"
          :key="img.id"
          :data-name="img.username"
        >
          <router-link
            :to="{
              name: 'postZoom',
              params: { id: img.id },
              query: {
                token: this.token,
                loggedUsername: this.username,
              },
            }"
          >
            <img :src="img.image" />
          </router-link>
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
      profilePicture: require("@/assets/default_PFP.png"),
      imageList: [],
      showMyImages: false,
      showUserDropdown: false,
      showSortDropdown: false,
      username: "notLoggedIn",
      userID: "",
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

        return this.imageList.filter((img) => {
          return img.postTags.some((tag) =>
            tag.toLowerCase().includes(searchTerm)
          );
        });
      } else {
        return this.imageList;
      }
    },
    myImagesList() {
      return this.imageList.filter((img) => img.username === this.username);
    },
  },
  methods: {
    toggleUserDropdown(event) {
      if (event) {
        event.stopPropagation();
      }
      this.showUserDropdown = !this.showUserDropdown;
    },
    closeUserDropdown(event) {
      if (!event.target.classList.contains("options-button")) {
        this.showUserDropdown = false;
      }
    },
    toggleSortDropdown(event) {
      if (event) {
        event.stopPropagation();
      }
      this.showSortDropdown = !this.showSortDropdown;
    },
    sortImagesByUploadDate(ascending) {
      this.imageList.sort((a, b) => {
        const dateA = new Date(a.postDate);
        const dateB = new Date(b.postDate);

        if (ascending) {
          return dateA - dateB;
        } else {
          return dateB - dateA;
        }
      });
    },
    closeSortDropdown(event) {
      if (!event.target.classList.contains("sort-button")) {
        this.showSortDropdown = false;
      }
    },
    closeUploadImageForm(data) {
      this.showUploadImageForm = false;
      this.postedImageID = data.imageID;
      //Check if image has been posted
      if (data.hasPosted) {
        //post image with all the data + the image ID to the backend DATABASE here
        const path = this.backendPath + "/publicaciones";
        const headers = { Authorization: "Bearer " + this.token };
        const dbData = {
          titulo: data.imageTitle,
          descripcion: data.imageDescription,
          imagen_url: data.imageID,
          usuario_nombre: data.username,
          tags: JSON.stringify(data.imageTags),
        };
        axios
          .post(path, dbData, { headers })
          .then((response) => {
            if (response.status === 200) {
              alert("Image uploaded successfully!");
              this.getPublication();
            }
          })
          .catch((error) => {
            alert("Error: " + error.response.data.message);
          });
      }
    },
    getPublication() {
      this.imageList = [];
      const pathPublications = this.backendPath + "/publicaciones";

      axios
        .get(pathPublications)
        .then((res) => {
          var publications = res.data.filter((publi) => {
            return publi.id != null;
          });
          for (let i = 0; i < publications.length; i++) {
            //Use publication data to recover image from Firebase and create the card
            const postedImageRef = firebaseRef(
              storage,
              "postedImages/" + publications[i].imagen_url
            );
            getDownloadURL(postedImageRef).then((url) => {
              let image = {
                id: publications[i].id,
                image: url,
                description: publications[i].descripcion,
                title: publications[i].titulo,
                username: publications[i].usuario_nombre,
                postDate: publications[i].fecha_creacion,
                postTags: JSON.parse(publications[i].tags),
              };
              this.imageList.push(image);
            });
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getUserInfo() {
      this.userID = this.$route.query.user_id;
      const pathUser = this.backendPath + "/usuario/" + this.userID;
      axios
        .get(pathUser)
        .then((response) => {
          this.username = response.data.nombre;
          const profilePictureRef = firebaseRef(
            storage,
            response.data.imagen_perfil_url
          );
          getDownloadURL(profilePictureRef).then((url) => {
            this.profilePicture = url;
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    window.addEventListener("click", this.closeUserDropdown);
    window.addEventListener("click", this.closeSortDropdown);
    this.getPublication();
  },
  beforeUnmount() {
    window.removeEventListener("click", this.closeUserDropdown);
  },
  created() {
    this.token = this.$route.query.token;
    if (typeof this.token === "undefined") {
      this.$router.push({ path: "/" });
    } else {
      this.getUserInfo();
    }
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
  max-width: 100%;
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

.sort-button {
  margin-top: 10px;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  display: flex;
  background-color: rgba(20, 117, 236, 0.9);
  padding: 0px 5px;
}

.sort-icon {
  height: 2rem;
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
  max-width: 100%;
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

.post-button-my-images-selected {
  background-color: white;
  border: none;
  color: rgba(20, 117, 236, 0.9);
  font-size: 16px;
  padding: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  width: 100%;
  margin-top: 20px;
  border-radius: 6px;
}

.post-button-my-images-selected .sidebar-icon {
  filter: none;
}

.post-button i {
  margin-right: 5px;
}

.post-button:hover {
  color: rgba(20, 117, 236, 0.9);
  background-color: white;
  transition: background-color 0.2s linear;
}
.sidebar-icon {
  margin-right: 5px;
  height: 1.1rem;
  filter: invert(1) grayscale(100%);
}

.post-button:hover .sidebar-icon {
  filter: none;
}
</style>
